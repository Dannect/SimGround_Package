import os
import json
import chardet
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================
# #region 프로젝트 폴더 및 패키지 정보 (최상단에 위치)
# =========================
project_dirs = [
    r"E:\TDS",
    # 40개 프로젝트 경로를 여기에 추가하세요
    # 예시:
    # r"E:\Project1",
    # r"E:\Project2",
    # r"E:\Project3",
    # ... 계속 추가
    
    # 자동 스캔 기능을 원한다면 아래 함수를 사용하세요
    # get_unity_projects_from_directory(r"E:\UnityProjects")
]

def get_unity_projects_from_directory(base_dir):
    """지정된 디렉토리에서 Unity 프로젝트들을 자동으로 찾습니다."""
    unity_projects = []
    
    if not os.path.exists(base_dir):
        print(f"기본 디렉토리가 존재하지 않습니다: {base_dir}")
        return unity_projects
    
    try:
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                # Unity 프로젝트인지 확인 (ProjectSettings 폴더 존재 여부)
                project_settings = os.path.join(item_path, "ProjectSettings")
                assets_folder = os.path.join(item_path, "Assets")
                
                if os.path.exists(project_settings) and os.path.exists(assets_folder):
                    unity_projects.append(item_path)
                    print(f"Unity 프로젝트 발견: {item}")
    
    except Exception as e:
        print(f"디렉토리 스캔 오류: {e}")
    
    return unity_projects

# 자동 스캔을 사용하려면 아래 주석을 해제하고 경로를 수정하세요
# project_dirs.extend(get_unity_projects_from_directory(r"E:\UnityProjects"))

git_packages = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    # 필요시 추가
}

# Git 설정
GIT_BASE_URL = "https://github.com/Dannect/"
DEFAULT_BRANCH = "main"
DEV_BRANCH = "dev"

# Unity CLI 설정
UNITY_EDITOR_PATH = r"C:\Program Files\Unity\Hub\Editor\2022.3.45f1\Editor\Unity.exe"  # Unity 설치 경로
UNITY_TIMEOUT = 300  # Unity 실행 타임아웃 (초)
UNITY_LOG_LEVEL = "info"  # Unity 로그 레벨 (debug, info, warning, error)
# endregion

# =========================
# #region Git 유틸리티 함수들
# =========================
def run_git_command(command, cwd):
    """Git 명령어를 실행하고 결과를 반환합니다."""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            shell=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def get_project_name_from_path(project_path):
    """프로젝트 경로에서 프로젝트명을 추출합니다."""
    return os.path.basename(project_path.rstrip(os.sep))

def get_repository_url(project_path):
    """프로젝트 경로를 기반으로 Git 리포지토리 URL을 생성합니다."""
    project_name = get_project_name_from_path(project_path)
    return f"{GIT_BASE_URL}{project_name}"

def is_git_repository(project_path):
    """해당 경로가 Git 리포지토리인지 확인합니다."""
    git_dir = os.path.join(project_path, ".git")
    return os.path.exists(git_dir)

def initialize_git_repository(project_path):
    """Git 리포지토리를 초기화하고 원격 저장소를 설정합니다."""
    print(f"Git 리포지토리 초기화 중: {project_path}")
    
    # Git 초기화
    success, stdout, stderr = run_git_command("git init", project_path)
    if not success:
        print(f"Git 초기화 실패: {stderr}")
        return False
    
    # 원격 저장소 추가
    repo_url = get_repository_url(project_path)
    success, stdout, stderr = run_git_command(f"git remote add origin {repo_url}", project_path)
    if not success and "already exists" not in stderr:
        print(f"원격 저장소 추가 실패: {stderr}")
        return False
    
    print(f"Git 리포지토리 초기화 완료: {repo_url}")
    return True

def get_current_branch(project_path):
    """현재 브랜치명을 가져옵니다."""
    success, stdout, stderr = run_git_command("git branch --show-current", project_path)
    if success:
        return stdout.strip()
    return None

def get_all_branches(project_path):
    """모든 브랜치 목록을 가져옵니다."""
    success, stdout, stderr = run_git_command("git branch -a", project_path)
    if success:
        branches = []
        for line in stdout.split('\n'):
            line = line.strip()
            if line and not line.startswith('*'):
                # 원격 브랜치 정보 제거
                branch = line.replace('remotes/origin/', '').strip()
                if branch and branch not in branches:
                    branches.append(branch)
        return branches
    return []

def get_branch_hierarchy_info(project_path, branch_name):
    """브랜치의 계층 정보를 가져옵니다 (커밋 수와 최근 커밋 시간)."""
    # 브랜치의 커밋 수 가져오기
    success, commit_count, stderr = run_git_command(f"git rev-list --count {branch_name}", project_path)
    if not success:
        return 0, 0
    
    # 브랜치의 최근 커밋 시간 가져오기 (Unix timestamp)
    success, last_commit_time, stderr = run_git_command(f"git log -1 --format=%ct {branch_name}", project_path)
    if not success:
        return int(commit_count) if commit_count.isdigit() else 0, 0
    
    return (
        int(commit_count) if commit_count.isdigit() else 0,
        int(last_commit_time) if last_commit_time.isdigit() else 0
    )

def find_deepest_branch(project_path, branches):
    """브랜치 계층구조에서 가장 깊은(아래) 브랜치를 찾습니다."""
    if not branches:
        return None
    
    # main 브랜치 제외
    filtered_branches = [b for b in branches if b != DEFAULT_BRANCH]
    if not filtered_branches:
        return None
    
    deepest_branch = None
    max_commits = 0
    latest_time = 0
    
    print("브랜치 계층 분석 중...")
    
    for branch in filtered_branches:
        commit_count, last_commit_time = get_branch_hierarchy_info(project_path, branch)
        print(f"  {branch}: {commit_count}개 커밋, 최근 커밋: {last_commit_time}")
        
        # 커밋 수가 더 많거나, 커밋 수가 같으면 더 최근 브랜치 선택
        if (commit_count > max_commits or 
            (commit_count == max_commits and last_commit_time > latest_time)):
            max_commits = commit_count
            latest_time = last_commit_time
            deepest_branch = branch
    
    return deepest_branch

def branch_exists(project_path, branch_name):
    """특정 브랜치가 존재하는지 확인합니다."""
    success, stdout, stderr = run_git_command(f"git show-ref --verify --quiet refs/heads/{branch_name}", project_path)
    return success

def create_and_checkout_branch(project_path, branch_name):
    """새 브랜치를 생성하고 체크아웃합니다."""
    print(f"브랜치 생성 및 체크아웃: {branch_name}")
    success, stdout, stderr = run_git_command(f"git checkout -b {branch_name}", project_path)
    if success:
        print(f"브랜치 '{branch_name}' 생성 완료")
        return True
    else:
        print(f"브랜치 생성 실패: {stderr}")
        return False

def checkout_branch(project_path, branch_name):
    """기존 브랜치로 체크아웃합니다."""
    print(f"브랜치 체크아웃: {branch_name}")
    success, stdout, stderr = run_git_command(f"git checkout {branch_name}", project_path)
    if success:
        print(f"브랜치 '{branch_name}'로 체크아웃 완료")
        return True
    else:
        print(f"브랜치 체크아웃 실패: {stderr}")
        # 다양한 Git 문제 처리
        if ("index" in stderr.lower() or "resolve" in stderr.lower() or 
            "untracked working tree files" in stderr.lower() or 
            "would be overwritten" in stderr.lower()):
            print("Git 상태 문제 감지, 정리 후 체크아웃 재시도...")
            if reset_git_index(project_path):
                success, stdout, stderr = run_git_command(f"git checkout {branch_name}", project_path)
                if success:
                    print(f"브랜치 '{branch_name}'로 체크아웃 완료 (재시도)")
                    return True
                else:
                    print(f"브랜치 체크아웃 재시도 실패: {stderr}")
                    # 강제 체크아웃 시도
                    print("강제 체크아웃 시도...")
                    success, stdout, stderr = run_git_command(f"git checkout -f {branch_name}", project_path)
                    if success:
                        print(f"브랜치 '{branch_name}'로 강제 체크아웃 완료")
                        return True
                    else:
                        print(f"강제 체크아웃도 실패: {stderr}")
                        return False
            else:
                return False
        else:
            return False

def get_target_branch(project_path):
    """커밋할 대상 브랜치를 결정합니다."""
    branches = get_all_branches(project_path)
    
    # 1. 브랜치 계층구조에서 가장 깊은(아래) 브랜치 찾기
    deepest_branch = find_deepest_branch(project_path, branches)
    if deepest_branch:
        print(f"계층구조에서 가장 깊은 브랜치 사용: {deepest_branch}")
        return deepest_branch
    
    # 2. 다른 브랜치가 없으면 dev 브랜치 확인
    if DEV_BRANCH in branches:
        print(f"dev 브랜치 사용")
        return DEV_BRANCH
    
    # 3. dev 브랜치도 없으면 dev 브랜치 생성
    print(f"적절한 브랜치가 없어 dev 브랜치를 새로 생성합니다")
    return DEV_BRANCH

def check_git_status(project_path):
    """Git 상태를 자세히 확인합니다."""
    print("Git 상태 상세 확인 중...")
    
    # 기본 상태 확인
    success, stdout, stderr = run_git_command("git status", project_path)
    if success:
        print("Git 상태:")
        for line in stdout.split('\n')[:10]:  # 처음 10줄만 출력
            if line.strip():
                print(f"  {line}")
    
    # 병합 상태 확인
    success, stdout, stderr = run_git_command("git status --porcelain", project_path)
    if success:
        conflict_files = [line for line in stdout.split('\n') if line.startswith('UU') or line.startswith('AA')]
        if conflict_files:
            print(f"충돌 파일 발견: {len(conflict_files)}개")
            return "conflict"
    
    return "normal"

def clean_untracked_files(project_path):
    """Untracked 파일들을 정리합니다."""
    print("Untracked 파일 정리 중...")
    
    # 먼저 어떤 파일들이 있는지 확인
    success, stdout, stderr = run_git_command("git clean -n", project_path)
    if success and stdout.strip():
        print("정리될 파일들:")
        for line in stdout.split('\n')[:10]:  # 처음 10개만 표시
            if line.strip():
                print(f"  {line}")
    
    # Untracked 파일들 제거 (디렉토리 포함)
    success, stdout, stderr = run_git_command("git clean -fd", project_path)
    if success:
        print("Untracked 파일 정리 완료")
        return True
    else:
        print(f"Untracked 파일 정리 실패: {stderr}")
        return False

def reset_git_index(project_path):
    """Git 인덱스 상태를 리셋합니다."""
    print("Git 인덱스 상태 리셋 중...")
    
    # 상세 상태 확인
    status = check_git_status(project_path)
    
    if status == "conflict":
        print("병합 충돌 감지, 자동 해결 시도...")
        # 병합 중단
        run_git_command("git merge --abort", project_path)
        # rebase 중단도 시도
        run_git_command("git rebase --abort", project_path)
    
    # Untracked 파일들 정리
    clean_untracked_files(project_path)
    
    # 인덱스 리셋
    success, stdout, stderr = run_git_command("git reset", project_path)
    if success:
        print("Git 인덱스 리셋 완료")
        return True
    else:
        print(f"Git 인덱스 리셋 실패: {stderr}")
        # 강제 리셋 시도
        print("강제 리셋 시도...")
        success, stdout, stderr = run_git_command("git reset --hard HEAD", project_path)
        if success:
            print("강제 리셋 완료")
            # 강제 리셋 후에도 untracked 파일 정리
            clean_untracked_files(project_path)
            return True
        else:
            print(f"강제 리셋도 실패: {stderr}")
            return False

def commit_and_push_changes(project_path, commit_message="Auto commit: Unity project updates"):
    """변경사항을 커밋하고 푸시합니다."""
    project_name = get_project_name_from_path(project_path)
    print(f"\n=== {project_name} Git 작업 시작 ===")
    
    # Git 리포지토리 확인 및 초기화
    if not is_git_repository(project_path):
        if not initialize_git_repository(project_path):
            print(f"Git 리포지토리 초기화 실패: {project_path}")
            return False
    
    # Git 상태 확인 및 문제 해결
    success, stdout, stderr = run_git_command("git status --porcelain", project_path)
    if not success:
        print(f"Git 상태 확인 실패: {stderr}")
        # 인덱스 문제일 가능성이 있으므로 리셋 시도
        if not reset_git_index(project_path):
            return False
        # 다시 상태 확인
        success, stdout, stderr = run_git_command("git status --porcelain", project_path)
        if not success:
            print(f"Git 상태 확인 재시도 실패: {stderr}")
            return False
    
    if not stdout.strip():
        print(f"변경사항 없음: {project_name}")
        return True
    
    print(f"변경사항 발견: {project_name}")
    
    # 대상 브랜치 결정
    target_branch = get_target_branch(project_path)
    
    # 브랜치 존재 여부 확인 및 체크아웃
    if branch_exists(project_path, target_branch):
        if not checkout_branch(project_path, target_branch):
            return False
    else:
        if not create_and_checkout_branch(project_path, target_branch):
            return False
    
    # 변경사항 스테이징
    success, stdout, stderr = run_git_command("git add .", project_path)
    if not success:
        print(f"Git add 실패: {stderr}")
        # 인덱스 문제일 가능성이 있으므로 리셋 후 재시도
        if "index" in stderr.lower() or "resolve" in stderr.lower():
            print("인덱스 문제 감지, 리셋 후 재시도...")
            if reset_git_index(project_path):
                success, stdout, stderr = run_git_command("git add .", project_path)
                if not success:
                    print(f"Git add 재시도 실패: {stderr}")
                    return False
            else:
                return False
        else:
            return False
    
    # 커밋
    success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"', project_path)
    if not success:
        print(f"Git commit 실패: {stderr}")
        return False
    
    print(f"커밋 완료: {project_name}")
    
    # 푸시
    success, stdout, stderr = run_git_command(f"git push -u origin {target_branch}", project_path)
    if not success:
        print(f"Git push 실패: {stderr}")
        return False
    
    print(f"푸시 완료: {project_name} -> {target_branch}")
    print(f"=== {project_name} Git 작업 완료 ===\n")
    return True
# endregion

# =========================
# #region Unity CLI 자동화 함수들
# =========================
def find_unity_editor_path():
    """Unity Editor 경로를 자동으로 찾습니다."""
    # 일반적인 Unity 설치 경로들
    common_paths = [
        r"C:\Program Files\Unity\Hub\Editor",
        r"C:\Program Files\Unity\Editor",
        r"C:\Program Files (x86)\Unity\Hub\Editor",
        r"C:\Program Files (x86)\Unity\Editor"
    ]
    
    for base_path in common_paths:
        if os.path.exists(base_path):
            # 버전 폴더들을 찾아서 가장 최신 버전 선택
            try:
                versions = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                if versions:
                    # 버전 정렬 (최신 버전 우선)
                    versions.sort(reverse=True)
                    unity_exe = os.path.join(base_path, versions[0], "Editor", "Unity.exe")
                    if os.path.exists(unity_exe):
                        return unity_exe
            except:
                continue
    
    return None

def run_unity_batch_mode(project_path, method_name=None, timeout=UNITY_TIMEOUT):
    """Unity를 배치 모드로 실행하여 Editor 스크립트를 실행합니다."""
    unity_path = UNITY_EDITOR_PATH
    
    # Unity 경로가 존재하지 않으면 자동 검색
    if not os.path.exists(unity_path):
        print(f"Unity 경로를 찾을 수 없습니다: {unity_path}")
        print("Unity 경로 자동 검색 중...")
        unity_path = find_unity_editor_path()
        if not unity_path:
            print("Unity Editor를 찾을 수 없습니다. UNITY_EDITOR_PATH를 확인해주세요.")
            return False
        print(f"Unity 경로 발견: {unity_path}")
    
    project_name = get_project_name_from_path(project_path)
    print(f"Unity 배치 모드 실행 중: {project_name}")
    
    # Unity 명령어 구성
    cmd = [
        unity_path,
        "-batchmode",           # 배치 모드
        "-quit",               # 완료 후 종료
        "-projectPath", project_path,  # 프로젝트 경로
        "-logFile", "-",       # 로그를 콘솔에 출력
    ]
    
    # 특정 메서드 실행이 지정된 경우
    if method_name:
        cmd.extend(["-executeMethod", method_name])
    
    try:
        print(f"Unity 명령어: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        
        # Unity 로그 출력
        if result.stdout:
            print("=== Unity 출력 ===")
            print(result.stdout)
        
        if result.stderr:
            print("=== Unity 오류 ===")
            print(result.stderr)
        
        # Unity는 성공해도 exit code가 0이 아닐 수 있음
        if result.returncode == 0:
            print(f"Unity 배치 모드 완료: {project_name}")
            return True
        else:
            print(f"Unity 배치 모드 경고 (exit code: {result.returncode}): {project_name}")
            # 로그에서 실제 오류 확인
            if "error" in result.stdout.lower() or "exception" in result.stdout.lower():
                print("실제 오류 발견, 실패로 처리")
                return False
            else:
                print("경고이지만 정상 처리된 것으로 판단")
                return True
                
    except subprocess.TimeoutExpired:
        print(f"Unity 실행 타임아웃 ({timeout}초): {project_name}")
        return False
    except Exception as e:
        print(f"Unity 실행 오류: {e}")
        return False

def process_unity_project_batch(project_path):
    """Unity 프로젝트를 배치 모드로 처리합니다."""
    project_name = get_project_name_from_path(project_path)
    
    if not os.path.exists(project_path):
        print(f"프로젝트 폴더가 존재하지 않습니다: {project_path}")
        return False
    
    # Unity 프로젝트인지 확인
    project_settings = os.path.join(project_path, "ProjectSettings", "ProjectSettings.asset")
    if not os.path.exists(project_settings):
        print(f"Unity 프로젝트가 아닙니다: {project_path}")
        return False
    
    print(f"\n=== {project_name} Unity 배치 처리 시작 ===")
    
    # Unity 배치 모드 실행 (패키지 임포트 및 Editor 스크립트 실행)
    success = run_unity_batch_mode(project_path)
    
    if success:
        print(f"=== {project_name} Unity 배치 처리 완료 ===")
        return True
    else:
        print(f"=== {project_name} Unity 배치 처리 실패 ===")
        return False

def create_unity_batch_script(project_path):
    """Unity Editor에서 실행할 배치 스크립트를 생성합니다."""
    script_dir = os.path.join(project_path, "Assets", "Editor", "BatchScripts")
    os.makedirs(script_dir, exist_ok=True)
    
    script_path = os.path.join(script_dir, "AutoBatchProcessor.cs")
    
    script_content = '''using UnityEngine;
using UnityEditor;
using System.IO;

public class AutoBatchProcessor
{
    [MenuItem("Tools/Process Batch")]
    public static void ProcessBatch()
    {
        Debug.Log("=== 배치 처리 시작 ===");
        
        // 패키지 임포트 대기
        AssetDatabase.Refresh();
        
        // PackageAssetCopier가 있다면 실행
        var copierType = System.Type.GetType("PackageAssetCopier");
        if (copierType != null)
        {
            var method = copierType.GetMethod("CopyFilesFromPackage", 
                System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
            if (method != null)
            {
                Debug.Log("PackageAssetCopier.CopyFilesFromPackage 실행");
                method.Invoke(null, null);
            }
        }
        
        // 최종 Asset Database 갱신
        AssetDatabase.Refresh();
        AssetDatabase.SaveAssets();
        
        Debug.Log("=== 배치 처리 완료 ===");
    }
}
'''
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"배치 스크립트 생성 완료: {script_path}")
        return True
    except Exception as e:
        print(f"배치 스크립트 생성 실패: {e}")
        return False

def process_multiple_projects_parallel(project_dirs, max_workers=3):
    """여러 Unity 프로젝트를 병렬로 처리합니다."""
    print(f"\n=== 병렬 처리 시작 (최대 {max_workers}개 동시 실행) ===")
    
    success_count = 0
    fail_count = 0
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 모든 프로젝트를 병렬로 제출
        future_to_project = {
            executor.submit(process_unity_project_batch, project_dir): project_dir 
            for project_dir in project_dirs if os.path.exists(project_dir)
        }
        
        # 완료된 작업들을 처리
        for future in as_completed(future_to_project):
            project_dir = future_to_project[future]
            project_name = get_project_name_from_path(project_dir)
            
            try:
                result = future.result()
                if result:
                    success_count += 1
                    print(f"✅ {project_name} 병렬 처리 완료")
                else:
                    fail_count += 1
                    print(f"❌ {project_name} 병렬 처리 실패")
                results.append((project_name, result))
            except Exception as e:
                fail_count += 1
                print(f"❌ {project_name} 병렬 처리 예외: {e}")
                results.append((project_name, False))
    
    print(f"\n=== 병렬 처리 결과 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 처리: {success_count + fail_count}개")
    
    return results
# endregion

# =========================
# #region UTF-8 변환 함수
# =========================
def convert_to_utf8(filepath):
    # 파일의 원래 인코딩 감지
    with open(filepath, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding']
    # 이미 UTF-8이면 변환하지 않음
    if encoding and encoding.lower().replace('-', '') == 'utf8':
        return False  # 변환하지 않음
    # 감지된 인코딩으로 읽어서 UTF-8로 저장
    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True  # 변환함
# endregion

# =========================
# #region Git 패키지 추가 함수
# =========================
def add_git_packages_to_manifest(project_dir, git_packages):
    manifest_path = os.path.join(project_dir, "Packages", "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"{manifest_path} 없음")
        return

    # manifest.json 파일 열기
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    changed = False  # 변경 여부 플래그

    # 모든 Git 패키지 추가/수정
    for name, url in git_packages.items():
        # 이미 동일한 값이 있으면 건너뜀
        if name in manifest["dependencies"] and manifest["dependencies"][name] == url:
            print(f"{name} 이미 설치됨, 생략")
            continue
        manifest["dependencies"][name] = url
        changed = True

    # 변경된 경우에만 저장
    if changed:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        print(f"{manifest_path}에 패키지들 추가/수정 완료!")
    else:
        print(f"{manifest_path} 변경 없음 (모든 패키지 이미 설치됨)")
# endregion

# =========================
# #region 메인 실행부
# =========================

def print_usage():
    """사용법을 출력합니다."""
    print("=== Unity 프로젝트 자동화 도구 사용법 ===")
    print("python dannect.unity.toolkit.py [옵션]")
    print("")
    print("옵션:")
    print("  --help           이 도움말을 표시합니다")
    print("  --skip-git       Git 작업을 건너뜁니다 (UTF-8 변환과 패키지 추가만 실행)")
    print("  --git-only       Git 작업만 실행합니다 (UTF-8 변환과 패키지 추가 건너뜀)")
    print("  --unity-batch    Unity 배치 모드로 Editor 스크립트 실행 (40개 프로젝트 자동화)")
    print("  --full-auto      모든 작업 + Unity 배치 모드 실행 (완전 자동화)")
    print("  --parallel       Unity 배치 모드를 병렬로 실행 (빠른 처리, 메모리 사용량 증가)")
    print("")
    print("기본 동작:")
    print("1. C# 파일 UTF-8 변환")
    print("2. Unity 패키지 추가")
    print("3. Git 커밋 및 푸시 (계층구조 최하위 브랜치 또는 dev 브랜치)")
    print("")
    print("Unity 배치 모드 (--unity-batch, --full-auto):")
    print("- Unity Editor를 배치 모드로 실행하여 Editor 스크립트 자동 실행")
    print("- PackageAssetCopier 등의 [InitializeOnLoad] 스크립트 실행")
    print("- 40개 프로젝트를 순차적으로 자동 처리 (기본)")
    print("- --parallel 옵션으로 병렬 처리 가능 (3개씩 동시 실행)")
    print("- Unity GUI 없이 백그라운드에서 실행")
    print("")
    print("Git 브랜치 전략:")
    print("- 브랜치 계층구조에서 가장 깊은(아래) 브랜치를 우선 사용")
    print("- 커밋 수가 많고 최근에 작업된 브랜치 선택")
    print("- 적절한 브랜치가 없으면 dev 브랜치 사용/생성")
    print("=====================================")

def main():
    """메인 실행 함수"""
    # 도움말 요청 확인
    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        return
    
    print("=== Unity 프로젝트 자동화 도구 시작 ===\n")
    
    # 명령행 인수 확인
    skip_git = "--skip-git" in sys.argv
    git_only = "--git-only" in sys.argv
    unity_batch = "--unity-batch" in sys.argv
    full_auto = "--full-auto" in sys.argv
    parallel = "--parallel" in sys.argv
    
    if full_auto:
        print("완전 자동화 모드: 모든 작업 + Unity 배치 모드 실행...\n")
        unity_batch = True  # full_auto는 unity_batch 포함
    elif unity_batch:
        print("Unity 배치 모드만 실행합니다...\n")
        skip_git = True  # unity_batch만 실행할 때는 다른 작업 건너뜀
    elif git_only:
        print("Git 작업만 실행합니다...\n")
    elif skip_git:
        print("Git 작업을 건너뜁니다...\n")
    
    # 1. UTF-8 변환 (git-only가 아닌 경우에만 실행)
    if not git_only:
        print("1. C# 파일 UTF-8 변환 작업 시작...")
        for project_dir in project_dirs:
            project_name = get_project_name_from_path(project_dir)
            print(f"\n--- {project_name} UTF-8 변환 ---")
            
            root_dir = os.path.join(project_dir, "Assets")
            if not os.path.exists(root_dir):
                print(f"Assets 폴더 없음: {project_dir}")
                continue
                
            for subdir, _, files in os.walk(root_dir):
                for file in files:
                    if file.endswith('.cs'):
                        try:
                            changed = convert_to_utf8(os.path.join(subdir, file))
                            if changed:
                                print(f"  {file} 변환 완료")
                            else:
                                print(f"  {file} 이미 UTF-8, 변환 생략")
                        except Exception as e:
                            print(f"  {file} 변환 실패: {e}")

        # 2. 각 프로젝트에 패키지 추가
        print("\n2. Unity 패키지 추가 작업 시작...")
        for project_dir in project_dirs:
            project_name = get_project_name_from_path(project_dir)
            print(f"\n--- {project_name} 패키지 추가 ---")
            add_git_packages_to_manifest(project_dir, git_packages)

    # 3. Git 커밋 및 푸시 (skip-git가 아닌 경우에만 실행)
    if not skip_git:
        print("\n3. Git 커밋 및 푸시 작업 시작...")
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                commit_and_push_changes(project_dir, "Auto commit: Unity project updates and package additions")
            else:
                print(f"프로젝트 폴더 없음: {project_dir}")

    # 4. Unity 배치 모드 실행 (unity-batch 또는 full-auto인 경우에만 실행)
    if unity_batch:
        print("\n4. Unity 배치 모드 실행 시작...")
        print(f"총 {len(project_dirs)}개 프로젝트 처리 예정")
        
        # 모든 프로젝트에 배치 스크립트 생성
        print("배치 스크립트 생성 중...")
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                create_unity_batch_script(project_dir)
        
        if parallel:
            # 병렬 처리
            print("병렬 처리 모드로 실행합니다...")
            process_multiple_projects_parallel(project_dirs, max_workers=3)
        else:
            # 순차 처리 (기본)
            print("순차 처리 모드로 실행합니다...")
            success_count = 0
            fail_count = 0
            
            for i, project_dir in enumerate(project_dirs, 1):
                project_name = get_project_name_from_path(project_dir)
                print(f"\n[{i}/{len(project_dirs)}] {project_name} 처리 중...")
                
                if not os.path.exists(project_dir):
                    print(f"프로젝트 폴더 없음: {project_dir}")
                    fail_count += 1
                    continue
                
                # Unity 배치 모드 실행
                if process_unity_project_batch(project_dir):
                    success_count += 1
                    print(f"✅ {project_name} 처리 완료")
                else:
                    fail_count += 1
                    print(f"❌ {project_name} 처리 실패")
            
            print(f"\n=== Unity 배치 모드 결과 ===")
            print(f"성공: {success_count}개")
            print(f"실패: {fail_count}개")
            print(f"총 처리: {success_count + fail_count}개")
    
    print("\n=== 모든 작업 완료 ===")

if __name__ == "__main__":
    main()

# endregion 