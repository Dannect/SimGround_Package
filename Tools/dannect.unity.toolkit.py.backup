import os
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from string import Template


# =========================
# Configuration and Constants
# =========================
class Config:
    """전체 설정 및 상수 클래스"""
    # 프로젝트 경로
    PROJECT_DIRS = [
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.1.6_AbioticFactors",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.2.7_WindFormationModel",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.2.2_SolarAltitudeShadowLengthTemperature",
        # 추가 프로젝트 경로들...
    ]
    
    # Git 설정
    GIT_BASE_URL = "https://github.com/Dannect/"
    DEFAULT_BRANCH = "main"
    DEV_BRANCH = "dev"
    
    # Unity 설정
    UNITY_EDITOR_PATH = r"C:\Program Files\Unity\Hub\Editor\6000.0.59f2\Editor\Unity.exe"
    UNITY_TIMEOUT = 300
    BUILD_TIMEOUT = 7200
    BUILD_OUTPUT_DIR = r"C:\Users\wkzkx\Desktop\Lim\GitHub\Build"
    
    # WebGL 빌드 설정
    # Code Optimization: "RuntimeSpeed" 또는 "RuntimeSpeedWithLTO"
    WEBGL_CODE_OPTIMIZATION = "RuntimeSpeed"  # "RuntimeSpeed" 또는 "RuntimeSpeedWithLTO"
    
    # 패키지 설정
    GIT_PACKAGES = {
        "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    }
    
    # 커밋 메시지 템플릿
    COMMIT_MESSAGES = {
        "package_update": "FEAT: Unity 패키지 업데이트 및 자동 설정 적용",

        "system_manager_update": "FEAT: SystemManager 메소드 추가 및 기능 확장",
        "webgl_build": "BUILD: WebGL 빌드 설정 및 출력 파일 생성",
        "auto_general": "CHORE: 자동화 도구를 통한 프로젝트 업데이트",
        "batch_process": "CHORE: Unity 배치 모드 자동 처리 완료",
        "full_automation": "FEAT: 완전 자동화 처리 (패키지 + 설정 + 빌드)"
    }

# 호환성을 위한 전역 변수들
project_dirs = Config.PROJECT_DIRS

git_packages = Config.GIT_PACKAGES
GIT_BASE_URL = Config.GIT_BASE_URL
DEFAULT_BRANCH = Config.DEFAULT_BRANCH
DEV_BRANCH = Config.DEV_BRANCH
COMMIT_MESSAGES = Config.COMMIT_MESSAGES
UNITY_EDITOR_PATH = Config.UNITY_EDITOR_PATH
UNITY_TIMEOUT = Config.UNITY_TIMEOUT
BUILD_TIMEOUT = Config.BUILD_TIMEOUT
BUILD_OUTPUT_DIR = Config.BUILD_OUTPUT_DIR
WEBGL_CODE_OPTIMIZATION = Config.WEBGL_CODE_OPTIMIZATION

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
                project_settings = os.path.join(item_path, "ProjectSettings")
                assets_folder = os.path.join(item_path, "Assets")
                
                if os.path.exists(project_settings) and os.path.exists(assets_folder):
                    unity_projects.append(item_path)
                    print(f"Unity 프로젝트 발견: {item}")
    
    except Exception as e:
        print(f"디렉토리 스캔 오류: {e}")
    
    return unity_projects

# =========================
# #region Git 유틸리티 함수들
# =========================
class GitUtils:
    """Git 관련 유틸리티 클래스"""
    
    @staticmethod
    def run_command(command, cwd):
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
    
    @staticmethod
    def get_project_name(project_path):
        """프로젝트 경로에서 프로젝트명을 추출합니다."""
        return os.path.basename(project_path.rstrip(os.sep))
    
    @staticmethod
    def get_repository_url(project_path):
        """프로젝트 경로를 기반으로 Git 리포지토리 URL을 생성합니다."""
        project_name = GitUtils.get_project_name(project_path)
        return f"{GIT_BASE_URL}{project_name}"
    
    @staticmethod
    def is_repository(project_path):
        """해당 경로가 Git 리포지토리인지 확인합니다."""
        return os.path.exists(os.path.join(project_path, ".git"))
    
    @staticmethod
    def initialize_repository(project_path):
        """Git 리포지토리를 초기화하고 원격 저장소를 설정합니다."""
        print(f"Git 리포지토리 초기화 중: {project_path}")
        
        # Git 초기화
        success, stdout, stderr = GitUtils.run_command("git init", project_path)
        if not success:
            print(f"Git 초기화 실패: {stderr}")
            return False
        
        # 원격 저장소 추가
        repo_url = GitUtils.get_repository_url(project_path)
        success, stdout, stderr = GitUtils.run_command(f"git remote add origin {repo_url}", project_path)
        if not success and "already exists" not in stderr:
            print(f"원격 저장소 추가 실패: {stderr}")
            return False
        
        print(f"Git 리포지토리 초기화 완료: {repo_url}")
        return True

    @staticmethod
    def get_current_branch(project_path):
        """현재 브랜치명을 가져옵니다."""
        success, stdout, stderr = GitUtils.run_command("git branch --show-current", project_path)
        return stdout.strip() if success else None

    @staticmethod
    def get_all_branches(project_path):
        """모든 브랜치 목록을 가져옵니다."""
        success, stdout, stderr = GitUtils.run_command("git branch -a", project_path)
        if not success:
            return []
        
        branches = []
        for line in stdout.split('\n'):
            line = line.strip()
            if line and not line.startswith('*'):
                branch = line.replace('remotes/origin/', '').strip()
                if branch and branch not in branches:
                    branches.append(branch)
        return branches

    @staticmethod
    def get_branch_hierarchy_info(project_path, branch_name):
        """브랜치의 계층 정보를 가져옵니다 (커밋 수와 최근 커밋 시간)."""
        # 브랜치의 커밋 수 가져오기
        success, commit_count, stderr = GitUtils.run_command(f"git rev-list --count {branch_name}", project_path)
        if not success:
            return 0, 0
        
        # 브랜치의 최근 커밋 시간 가져오기 (Unix timestamp)
        success, last_commit_time, stderr = GitUtils.run_command(f"git log -1 --format=%ct {branch_name}", project_path)
        if not success:
            return int(commit_count) if commit_count.isdigit() else 0, 0
        
        return (
            int(commit_count) if commit_count.isdigit() else 0,
            int(last_commit_time) if last_commit_time.isdigit() else 0
        )

    @staticmethod
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
            commit_count, last_commit_time = GitUtils.get_branch_hierarchy_info(project_path, branch)
            print(f"  {branch}: {commit_count}개 커밋, 최근 커밋: {last_commit_time}")
            
            # 커밋 수가 더 많거나, 커밋 수가 같으면 더 최근 브랜치 선택
            if (commit_count > max_commits or 
                (commit_count == max_commits and last_commit_time > latest_time)):
                max_commits = commit_count
                latest_time = last_commit_time
                deepest_branch = branch
        
        return deepest_branch

    @staticmethod
    def branch_exists(project_path, branch_name):
        """특정 브랜치가 존재하는지 확인합니다."""
        success, stdout, stderr = GitUtils.run_command(f"git show-ref --verify --quiet refs/heads/{branch_name}", project_path)
        return success

    @staticmethod
    def create_and_checkout_branch(project_path, branch_name):
        """새 브랜치를 생성하고 체크아웃합니다."""
        print(f"브랜치 생성 및 체크아웃: {branch_name}")
        success, stdout, stderr = GitUtils.run_command(f"git checkout -b {branch_name}", project_path)
        if success:
            print(f"브랜치 '{branch_name}' 생성 완료")
            return True
        else:
            print(f"브랜치 생성 실패: {stderr}")
            return False

    @staticmethod
    def checkout_branch(project_path, branch_name):
        """기존 브랜치로 체크아웃합니다."""
        print(f"브랜치 체크아웃: {branch_name}")
        success, stdout, stderr = GitUtils.run_command(f"git checkout {branch_name}", project_path)
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
                if GitUtils.reset_git_index(project_path):
                    success, stdout, stderr = GitUtils.run_command(f"git checkout {branch_name}", project_path)
                    if success:
                        print(f"브랜치 '{branch_name}'로 체크아웃 완료 (재시도)")
                        return True
                    else:
                        print(f"브랜치 체크아웃 재시도 실패: {stderr}")
                        # 강제 체크아웃 시도
                        print("강제 체크아웃 시도...")
                        success, stdout, stderr = GitUtils.run_command(f"git checkout -f {branch_name}", project_path)
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

    @staticmethod
    def check_git_status(project_path):
        """Git 상태를 자세히 확인합니다."""
        print("Git 상태 상세 확인 중...")
        
        # 기본 상태 확인
        success, stdout, stderr = GitUtils.run_command("git status", project_path)
        if success:
            print("Git 상태:")
            for line in stdout.split('\n')[:10]:  # 처음 10줄만 출력
                if line.strip():
                    print(f"  {line}")
        
        # 병합 상태 확인
        success, stdout, stderr = GitUtils.run_command("git status --porcelain", project_path)
        if success:
            conflict_files = [line for line in stdout.split('\n') if line.startswith('UU') or line.startswith('AA')]
            if conflict_files:
                print(f"충돌 파일 발견: {len(conflict_files)}개")
                return "conflict"
        
        return "normal"

    @staticmethod
    def clean_untracked_files(project_path):
        """Untracked 파일들을 정리합니다."""
        print("Untracked 파일 정리 중...")
        
        # 먼저 어떤 파일들이 있는지 확인
        success, stdout, stderr = GitUtils.run_command("git clean -n", project_path)
        if success and stdout.strip():
            print("정리될 파일들:")
            for line in stdout.split('\n')[:10]:  # 처음 10개만 표시
                if line.strip():
                    print(f"  {line}")
        
        # Untracked 파일들 제거 (디렉토리 포함)
        success, stdout, stderr = GitUtils.run_command("git clean -fd", project_path)
        if success:
            print("Untracked 파일 정리 완료")
            return True
        else:
            print(f"Untracked 파일 정리 실패: {stderr}")
            return False

    @staticmethod
    def reset_git_index(project_path):
        """Git 인덱스 상태를 리셋합니다."""
        print("Git 인덱스 상태 리셋 중...")
        
        # 상세 상태 확인
        status = GitUtils.check_git_status(project_path)
        
        if status == "conflict":
            print("병합 충돌 감지, 자동 해결 시도...")
            # 병합 중단
            GitUtils.run_command("git merge --abort", project_path)
            # rebase 중단도 시도
            GitUtils.run_command("git rebase --abort", project_path)
        
        # Untracked 파일들 정리
        GitUtils.clean_untracked_files(project_path)
        
        # 인덱스 리셋
        success, stdout, stderr = GitUtils.run_command("git reset", project_path)
        if success:
            print("Git 인덱스 리셋 완료")
            return True
        else:
            print(f"Git 인덱스 리셋 실패: {stderr}")
            # 강제 리셋 시도
            print("강제 리셋 시도...")
            success, stdout, stderr = GitUtils.run_command("git reset --hard HEAD", project_path)
            if success:
                print("강제 리셋 완료")
                # 강제 리셋 후에도 untracked 파일 정리
                GitUtils.clean_untracked_files(project_path)
                return True
            else:
                print(f"강제 리셋도 실패: {stderr}")
                return False


# 호환성을 위한 래퍼 함수들
def run_git_command(command, cwd):
    return GitUtils.run_command(command, cwd)

def get_project_name_from_path(project_path):
    return GitUtils.get_project_name(project_path)

def get_repository_url(project_path):
    return GitUtils.get_repository_url(project_path)

def is_git_repository(project_path):
    return GitUtils.is_repository(project_path)

def initialize_git_repository(project_path):
    return GitUtils.initialize_repository(project_path)

# 호환성을 위한 래퍼 함수들 (계속)
def get_current_branch(project_path):
    return GitUtils.get_current_branch(project_path)

def get_all_branches(project_path):
    return GitUtils.get_all_branches(project_path)

def get_branch_hierarchy_info(project_path, branch_name):
    return GitUtils.get_branch_hierarchy_info(project_path, branch_name)

def find_deepest_branch(project_path, branches):
    return GitUtils.find_deepest_branch(project_path, branches)

def branch_exists(project_path, branch_name):
    return GitUtils.branch_exists(project_path, branch_name)

def create_and_checkout_branch(project_path, branch_name):
    return GitUtils.create_and_checkout_branch(project_path, branch_name)

def checkout_branch(project_path, branch_name):
    return GitUtils.checkout_branch(project_path, branch_name)

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

# 중복 함수 제거됨 - GitUtils 클래스 메소드 사용

def check_git_status(project_path):
    return GitUtils.check_git_status(project_path)

def clean_untracked_files(project_path):
    return GitUtils.clean_untracked_files(project_path)

def reset_git_index(project_path):
    return GitUtils.reset_git_index(project_path)

def commit_changes(project_path, commit_message_type="auto_general", custom_message=None):
    """변경사항을 커밋합니다 (푸시 제외)."""
    project_name = get_project_name_from_path(project_path)
    print(f"\n=== {project_name} Git 커밋 시작 ===")
    
    # 커밋 메시지 결정
    if custom_message:
        commit_message = custom_message
    else:
        commit_message = COMMIT_MESSAGES.get(commit_message_type, COMMIT_MESSAGES["auto_general"])
    
    print(f"📝 커밋 메시지: {commit_message}")
    
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
    print(f"=== {project_name} Git 커밋 완료 ===\n")
    return True

def push_changes(project_path):
    """커밋된 변경사항을 푸시합니다."""
    project_name = get_project_name_from_path(project_path)
    print(f"\n=== {project_name} Git 푸시 시작 ===")
    
    # Git 리포지토리 확인
    if not is_git_repository(project_path):
        print(f"Git 리포지토리가 아닙니다: {project_path}")
        return False
    
    # 현재 브랜치 확인
    current_branch = get_current_branch(project_path)
    if not current_branch:
        print(f"현재 브랜치를 확인할 수 없습니다: {project_path}")
        return False
    
    print(f"현재 브랜치: {current_branch}")
    
    # 푸시할 커밋이 있는지 확인
    success, stdout, stderr = run_git_command(f"git log origin/{current_branch}..HEAD --oneline", project_path)
    if not success:
        print(f"푸시할 커밋 확인 실패: {stderr}")
        print("원격 브랜치가 없거나 첫 푸시일 수 있습니다.")
    elif not stdout.strip():
        print(f"푸시할 커밋 없음: {project_name}")
        return True
    else:
        print(f"푸시할 커밋 발견: {len(stdout.strip().split('\n'))}개")
    
    # 푸시
    success, stdout, stderr = run_git_command(f"git push -u origin {current_branch}", project_path)
    if not success:
        print(f"Git push 실패: {stderr}")
        return False
    
    print(f"푸시 완료: {project_name} -> {current_branch}")
    print(f"=== {project_name} Git 푸시 완료 ===\n")
    return True

def commit_and_push_changes(project_path, commit_message_type="auto_general", custom_message=None):
    """변경사항을 커밋하고 푸시합니다 (기존 호환성 유지)."""
    if not commit_changes(project_path, commit_message_type, custom_message):
        return False
    return push_changes(project_path)
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
    
    # Unity 배치 모드 실행 (패키지 임포트 및 프로젝트 설정 검증)
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
        
        // 패키지 임포트 및 Asset Database 갱신
        AssetDatabase.Refresh();
        
        // 프로젝트 설정 검증
        ValidateProjectSettings();
        
        // 최종 Asset Database 갱신
        AssetDatabase.Refresh();
        AssetDatabase.SaveAssets();
        
        Debug.Log("=== 배치 처리 완료 ===");
    }
    
    private static void ValidateProjectSettings()
    {
        Debug.Log("프로젝트 설정 검증 중...");
        
        // 기본 프로젝트 설정 확인
        if (string.IsNullOrEmpty(PlayerSettings.productName))
        {
            Debug.LogWarning("제품명이 설정되지 않았습니다.");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.companyName))
        {
            Debug.LogWarning("회사명이 설정되지 않았습니다.");
        }
        
        Debug.Log("프로젝트 설정 검증 완료");
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
# #region SystemManager 메소드 추가 함수들
# =========================

# SystemManager에 추가할 메소드 템플릿들
SYSTEM_MANAGER_METHODS = {
    "AllowKeyboardInput": '''    public void AllowKeyboardInput(bool isAllow)
    {
        Debug.Log("AllowKeyboardInput!" + isAllow);
#if UNITY_WEBGL && !UNITY_EDITOR
        WebGLInput.captureAllKeyboardInput = isAllow;
#endif
    }''',
    
    # 다른 메소드들도 여기에 추가 가능
    # "OtherMethod": '''    public void OtherMethod()
    # {
    #     // 메소드 내용
    # }''',
}

def find_system_manager_files(project_dirs):
    """모든 프로젝트에서 SystemManager.cs 파일들을 찾습니다."""
    system_manager_files = []
    
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            continue
            
        assets_dir = os.path.join(project_dir, "Assets")
        if not os.path.exists(assets_dir):
            continue
        
        project_name = get_project_name_from_path(project_dir)
        
        # Assets 폴더에서 SystemManager.cs 파일 찾기
        for root, dirs, files in os.walk(assets_dir):
            # Library, Temp 등 불필요한 폴더 제외
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Library', 'Temp', 'Logs']]
            
            for file in files:
                if file == "SystemManager.cs":
                    filepath = os.path.join(root, file)
                    system_manager_files.append((project_name, filepath))
                    print(f"SystemManager 발견: {project_name} - {os.path.relpath(filepath, project_dir)}")
    
    return system_manager_files

def has_method(filepath, method_name):
    """스크립트에 특정 메소드가 이미 존재하는지 확인합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 메소드 시그니처 패턴들 (다양한 접근 제한자와 형태 고려)
        import re
        patterns = [
            rf'(public|private|protected|internal)?\s*(static)?\s*(void|bool|int|float|string|[A-Z]\w*)\s+{method_name}\s*\(',
            rf'{method_name}\s*\(',  # 단순 패턴도 확인
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
        
    except Exception as e:
        print(f"메소드 존재 확인 실패 ({filepath}): {e}")
        return True  # 오류 시 안전하게 이미 존재한다고 가정

def add_method_to_script(filepath, method_name, method_content):
    """스크립트의 클래스 끝에 메소드를 추가합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 클래스의 마지막 닫는 중괄호 찾기 (더 안전한 방식)
        lines = content.split('\n')
        
        # 클래스 선언 찾기
        class_start_line = -1
        for i, line in enumerate(lines):
            if ('class ' in line and 'SystemManager' in line) or ('public class' in line):
                class_start_line = i
                break
        
        if class_start_line == -1:
            print(f"클래스 선언을 찾을 수 없습니다: {filepath}")
            return False
        
        # 클래스 시작 이후에서 마지막 중괄호 찾기
        last_brace_index = -1
        brace_count = 0
        in_class = False
        
        for i in range(class_start_line, len(lines)):
            line = lines[i].strip()
            
            # 클래스 시작 중괄호 찾기
            if not in_class and '{' in line:
                in_class = True
                brace_count = 1
                continue
            
            if in_class:
                # 중괄호 계산
                brace_count += line.count('{')
                brace_count -= line.count('}')
                
                # 클래스가 끝나는 지점 (brace_count가 0이 되는 지점)
                if brace_count == 0:
                    last_brace_index = i
                    break
        
        if last_brace_index == -1:
            print(f"클래스 닫는 중괄호를 찾을 수 없습니다: {filepath}")
            return False
        
        # 메소드 추가 (닫는 중괄호 바로 전에)
        lines.insert(last_brace_index, "")  # 빈 줄 추가
        lines.insert(last_brace_index + 1, method_content)
        
        # 파일에 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return True
        
    except Exception as e:
        print(f"메소드 추가 실패 ({filepath}): {e}")
        return False

def add_methods_to_system_managers(project_dirs, method_names=None):
    """모든 SystemManager에 지정된 메소드들을 추가합니다."""
    if method_names is None:
        method_names = ["AllowKeyboardInput"]  # 기본값
    
    print(f"\n=== SystemManager 메소드 추가 시작 ===")
    print(f"추가할 메소드: {', '.join(method_names)}")
    
    # SystemManager 파일들 찾기
    system_manager_files = find_system_manager_files(project_dirs)
    
    if not system_manager_files:
        print("SystemManager.cs 파일을 찾을 수 없습니다.")
        return False
    
    print(f"총 {len(system_manager_files)}개 SystemManager 파일 발견")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for project_name, filepath in system_manager_files:
        print(f"\n--- {project_name} SystemManager 처리 ---")
        
        methods_added = []
        methods_skipped = []
        
        for method_name in method_names:
            if method_name not in SYSTEM_MANAGER_METHODS:
                print(f"  ❌ 알 수 없는 메소드: {method_name}")
                continue
            
            # 메소드가 이미 존재하는지 확인
            if has_method(filepath, method_name):
                print(f"  ⚪ {method_name}: 이미 존재함, 생략")
                methods_skipped.append(method_name)
                continue
            
            # 메소드 추가
            method_content = SYSTEM_MANAGER_METHODS[method_name]
            if add_method_to_script(filepath, method_name, method_content):
                print(f"  ✅ {method_name}: 추가 완료")
                methods_added.append(method_name)
            else:
                print(f"  ❌ {method_name}: 추가 실패")
        
        # 결과 집계
        if methods_added:
            success_count += 1
            print(f"  📊 {project_name}: {len(methods_added)}개 메소드 추가됨")
        elif methods_skipped:
            skip_count += 1
            print(f"  📊 {project_name}: 모든 메소드가 이미 존재함")
        else:
            fail_count += 1
            print(f"  📊 {project_name}: 메소드 추가 실패")
    
    print(f"\n=== SystemManager 메소드 추가 결과 ===")
    print(f"성공 (메소드 추가됨): {success_count}개")
    print(f"생략 (이미 존재): {skip_count}개") 
    print(f"실패: {fail_count}개")
    print(f"총 처리: {len(system_manager_files)}개")
    
    return success_count > 0

def add_custom_method_to_system_managers(project_dirs, method_name, method_content):
    """사용자 정의 메소드를 SystemManager에 추가합니다."""
    print(f"\n=== 사용자 정의 메소드 추가: {method_name} ===")
    
    # 임시로 메소드 템플릿에 추가
    original_methods = SYSTEM_MANAGER_METHODS.copy()
    SYSTEM_MANAGER_METHODS[method_name] = method_content
    
    try:
        result = add_methods_to_system_managers(project_dirs, [method_name])
        return result
    finally:
        # 원래 템플릿으로 복원
        SYSTEM_MANAGER_METHODS.clear()
        SYSTEM_MANAGER_METHODS.update(original_methods)

def add_hello_world_method_to_system_manager(filepath):
    """SystemManager에 Hello World 메소드를 추가합니다."""
    hello_world_method = '''    private void PrintHelloWorld()
    {
        Debug.Log("Hello World!");
    }'''
    
    # 메소드가 이미 존재하는지 확인
    if has_method(filepath, "PrintHelloWorld"):
        print(f"  ⚪ PrintHelloWorld 메소드가 이미 존재합니다.")
        return True
    
    # 메소드 추가
    if add_method_to_script(filepath, "PrintHelloWorld", hello_world_method):
        print(f"  ✅ PrintHelloWorld 메소드 추가 완료")
        return True
    else:
        print(f"  ❌ PrintHelloWorld 메소드 추가 실패")
        return False

def add_hello_world_call_to_start_method(filepath):
    """SystemManager의 Start() 함수 가장 아래에 PrintHelloWorld() 호출을 추가합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Start() 메소드를 찾아서 그 끝에 PrintHelloWorld() 호출 추가
        lines = content.split('\n')
        
        # Start() 메소드 찾기 (더 정확한 패턴)
        start_method_found = False
        start_method_line = -1
        method_brace_count = 0
        start_method_end_line = -1
        start_brace_found = False
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Start() 메소드 시작 찾기 (더 정확한 패턴)
            if not start_method_found and ('void Start()' in line or 'void Start(' in line) and ('private' in line or 'public' in line or 'protected' in line or stripped_line.startswith('void')):
                start_method_found = True
                start_method_line = i
                print(f"  📍 Start() 메소드 발견: {start_method_line + 1}번째 줄")
                
                # 같은 줄에 중괄호가 있는지 확인
                if '{' in line:
                    start_brace_found = True
                    method_brace_count = 1
                continue
            
            # Start() 메소드 내부에서 중괄호 카운팅
            if start_method_found and start_method_end_line == -1:
                # 시작 중괄호를 아직 못 찾았다면 찾기
                if not start_brace_found and '{' in stripped_line:
                    start_brace_found = True
                    method_brace_count = 1
                    continue
                
                # 시작 중괄호를 찾았다면 중괄호 카운팅 시작
                if start_brace_found:
                    method_brace_count += stripped_line.count('{')
                    method_brace_count -= stripped_line.count('}')
                    
                    # Start() 메소드가 끝나는 지점
                    if method_brace_count == 0:
                        start_method_end_line = i
                        print(f"  📍 Start() 메소드 끝: {start_method_end_line + 1}번째 줄")
                        break
        
        if not start_method_found:
            print(f"  ❌ Start() 메소드를 찾을 수 없습니다.")
            return False
        
        if start_method_end_line == -1:
            print(f"  ❌ Start() 메소드의 끝을 찾을 수 없습니다.")
            return False
        
        # 이미 PrintHelloWorld() 호출이 있는지 확인
        start_method_content = '\n'.join(lines[start_method_line:start_method_end_line + 1])
        if 'PrintHelloWorld()' in start_method_content:
            print(f"  ⚪ Start() 메소드에 PrintHelloWorld() 호출이 이미 존재합니다.")
            return True
        
        # Start() 메소드 끝 바로 전에 PrintHelloWorld() 호출 추가
        # 닫는 중괄호 바로 전에 들여쓰기와 함께 추가
        indent = "        "  # 8칸 들여쓰기 (일반적인 메소드 내부 들여쓰기)
        
        # 기존 줄의 들여쓰기 패턴 분석 (Start() 메소드 내부에서)
        for check_line in range(start_method_end_line - 1, start_method_line, -1):
            if lines[check_line].strip() and not lines[check_line].strip().startswith('}'):
                # 비어있지 않고 닫는 중괄호가 아닌 줄의 들여쓰기 패턴을 가져옴
                leading_spaces = len(lines[check_line]) - len(lines[check_line].lstrip())
                if leading_spaces > 0:
                    indent = ' ' * leading_spaces
                    break
        
        lines.insert(start_method_end_line, f"{indent}PrintHelloWorld();")
        lines.insert(start_method_end_line, "")  # 빈 줄 추가
        
        # 파일에 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  ✅ Start() 메소드에 PrintHelloWorld() 호출 추가 완료")
        return True
        
    except Exception as e:
        print(f"  ❌ Start() 메소드 수정 실패: {e}")
        return False

def add_hello_world_to_all_system_managers(project_dirs):
    """모든 SystemManager에 Hello World 메소드를 추가하고 Start() 함수에서 호출하도록 설정합니다."""
    print(f"\n=== SystemManager Hello World 메소드 추가 시작 ===")
    
    # SystemManager 파일들 찾기
    system_manager_files = find_system_manager_files(project_dirs)
    
    if not system_manager_files:
        print("SystemManager.cs 파일을 찾을 수 없습니다.")
        return False
    
    print(f"총 {len(system_manager_files)}개 SystemManager 파일 발견")
    
    success_count = 0
    fail_count = 0
    
    for project_name, filepath in system_manager_files:
        print(f"\n--- {project_name} SystemManager 처리 ---")
        
        # 1. Hello World 메소드 추가
        method_added = add_hello_world_method_to_system_manager(filepath)
        
        # 2. Start() 함수에 호출 추가
        call_added = add_hello_world_call_to_start_method(filepath)
        
        # 결과 집계
        if method_added and call_added:
            success_count += 1
            print(f"  📊 {project_name}: Hello World 메소드 추가 및 Start() 호출 설정 완료")
        else:
            fail_count += 1
            print(f"  📊 {project_name}: Hello World 설정 실패")
    
    print(f"\n=== SystemManager Hello World 메소드 추가 결과 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 처리: {len(system_manager_files)}개")
    
    return success_count > 0

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
# #region Unity 빌드 자동화 함수들 (Player Settings 완전 반영)
# =========================
def create_unity_webgl_build_script(project_path, output_path=None, auto_configure=True, code_optimization=None):
    """Unity WebGL 빌드를 위한 Editor 스크립트를 생성합니다. (Player Settings 자동 설정 포함)"""
    editor_dir = os.path.join(project_path, "Assets", "Editor")
    if not os.path.exists(editor_dir):
        os.makedirs(editor_dir)
    
    script_path = os.path.join(editor_dir, "AutoWebGLBuildScript.cs")
    
    # 프로젝트명 추출
    project_name = get_project_name_from_path(project_path)
    
    if output_path is None:
        # 중앙 집중식 빌드 경로: C:\Users\wkzkx\Desktop\Lim\GitHub\Build\프로젝트명\
        output_path = os.path.join(BUILD_OUTPUT_DIR, project_name)
    
    output_path_formatted = output_path.replace(os.sep, '/')
    
    # Code Optimization 설정 (기본값 또는 매개변수로 전달된 값)
    if code_optimization is None:
        code_optimization = WEBGL_CODE_OPTIMIZATION
    
    # 유효성 검사
    if code_optimization not in ["RuntimeSpeed", "RuntimeSpeedWithLTO"]:
        print(f"⚠️ 잘못된 Code Optimization 설정: {code_optimization}, 기본값 'RuntimeSpeed' 사용")
        code_optimization = "RuntimeSpeed"
    
    # Template 시스템을 사용하여 Unity 스크립트 생성
    script_template = Template("""using UnityEngine;
using UnityEditor;
using UnityEditor.Build;
using System.IO;

public class AutoWebGLBuildScript
{
    // Code Optimization 설정: "RuntimeSpeed" 또는 "RuntimeSpeedWithLTO"
    // 이 값은 dannect.unity.toolkit.py의 Config.WEBGL_CODE_OPTIMIZATION에서 자동 설정됩니다
    private static string CODE_OPTIMIZATION_TYPE = "$code_optimization";
    
    [MenuItem("Build/Auto Build WebGL (Player Settings)")]
    public static void BuildWebGLWithPlayerSettings()
    {
        Debug.Log("=== WebGL Player Settings 자동 설정 및 빌드 시작 ===");
        
        // WebGL Player Settings 자동 설정
        ConfigureWebGLPlayerSettings();
        
        // 설정된 Player Settings 정보 출력
        LogCurrentPlayerSettings();
        
        // 프로젝트명 추출 (Unity에서 스크립트가 실행되는 프로젝트의 이름)
        string projectName = Application.productName;
        if (string.IsNullOrEmpty(projectName))
        {
            // ProductName이 없으면 프로젝트 폴더명 사용
            projectName = new DirectoryInfo(Application.dataPath).Parent.Name;
        }
        
        // 특수문자 제거 및 안전한 파일명 생성
        string safeProjectName = projectName.Replace(" ", "_");
        safeProjectName = System.Text.RegularExpressions.Regex.Replace(safeProjectName, @"[^\\w\\-_\\.]", "");
        
        // 중앙 집중식 빌드 경로 설정: C:/Users/wkzkx/Desktop/Lim/GitHub/Build/프로젝트명
        string buildPath = @"$output_path";
        
        // 출력 디렉토리 생성 (상위 폴더까지 모두 생성)
        try
        {
            if (!Directory.Exists(buildPath))
            {
                Directory.CreateDirectory(buildPath);
                Debug.Log("중앙 집중식 빌드 출력 디렉토리 생성: " + buildPath);
            }
            else
            {
                Debug.Log("중앙 집중식 빌드 출력 디렉토리 확인 완료: " + buildPath);
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError("빌드 출력 디렉토리 생성 실패: " + e.Message);
            Debug.LogError("경로: " + buildPath);
            return;
        }
        
        Debug.Log("📁 프로젝트명: " + projectName + " -> 안전한 파일명: " + safeProjectName);
        Debug.Log("🌐 중앙 집중식 빌드 경로: " + buildPath);
        
        // 빌드할 씬들 가져오기 (Build Settings에서 활성화된 씬만)
        string[] scenes = GetBuildScenes();
        if (scenes.Length == 0)
        {
            Debug.LogError("빌드할 씬이 없습니다. Build Settings에서 씬을 추가하세요.");
            return;
        }
        
        // WebGL 빌드 옵션 설정 (Player Settings 완전 반영)
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = scenes;
        buildPlayerOptions.locationPathName = buildPath;
        buildPlayerOptions.target = BuildTarget.WebGL;
        
        // 빌드 옵션을 Player Settings에 따라 설정
        buildPlayerOptions.options = GetBuildOptionsFromPlayerSettings();
        
        // WebGL 특수 설정 적용
        ApplyWebGLSettings();
        
        Debug.Log("🌐 WebGL 중앙 집중식 빌드 시작");
        Debug.Log("📁 중앙 빌드 경로: " + buildPlayerOptions.locationPathName);
        Debug.Log("📂 프로젝트명: " + safeProjectName);
        Debug.Log("🎮 제품명: " + PlayerSettings.productName);
        Debug.Log("🏢 회사명: " + PlayerSettings.companyName);
        Debug.Log("📋 버전: " + PlayerSettings.bundleVersion);
        
        // WebGL 빌드 실행
        var report = BuildPipeline.BuildPlayer(buildPlayerOptions);
        
        // 빌드 결과 확인
        if (report.summary.result == UnityEditor.Build.Reporting.BuildResult.Succeeded)
        {
            Debug.Log("✅ WebGL 중앙 집중식 빌드 성공!");
            Debug.Log("📦 빌드 크기: " + FormatBytes(report.summary.totalSize));
            Debug.Log("⏱️ 빌드 시간: " + report.summary.totalTime);
            Debug.Log("📁 중앙 빌드 경로: " + buildPath);
            Debug.Log("📂 프로젝트명: " + safeProjectName);
            Debug.Log("📄 주요 파일: " + safeProjectName + ".data, " + safeProjectName + ".wasm, index.html");
            Debug.Log("🌐 중앙 집중식 WebGL 빌드 완료!");
        }
        else
        {
            Debug.LogError("❌ WebGL 빌드 실패: " + report.summary.result);
            if (report.summary.totalErrors > 0)
            {
                Debug.LogError("에러 수: " + report.summary.totalErrors);
            }
            if (report.summary.totalWarnings > 0)
            {
                Debug.LogWarning("경고 수: " + report.summary.totalWarnings);
            }
        }
        
        Debug.Log("=== WebGL Player Settings 반영 빌드 완료 ===");
    }
    
    private static void ConfigureWebGLPlayerSettings()
    {
        Debug.Log("🔧 WebGL Player Settings 이미지 기반 고정 설정 적용 중...");
        
        // 기본 제품 정보 설정 (비어있는 경우에만)
        if (string.IsNullOrEmpty(PlayerSettings.productName))
        {
            PlayerSettings.productName = "Science Experiment Simulation";
            Debug.Log("✅ 제품명 설정: Science Experiment Simulation");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.companyName))
        {
            PlayerSettings.companyName = "Educational Software";
            Debug.Log("✅ 회사명 설정: Educational Software");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.bundleVersion))
        {
            PlayerSettings.bundleVersion = "1.0.0";
            Debug.Log("✅ 버전 설정: 1.0.0");
        }
        
        // === 이미지 기반 고정 설정 적용 ===
        
        // Resolution and Presentation 설정 (이미지 기반)
        PlayerSettings.defaultWebScreenWidth = 1655;
        PlayerSettings.defaultWebScreenHeight = 892;
        PlayerSettings.runInBackground = true;
        Debug.Log("✅ 해상도 설정: 1655x892, Run In Background 활성화");
        
        // WebGL Template 설정 (이미지 기반: Minimal)
        PlayerSettings.WebGL.template = "APPLICATION:Minimal";
        Debug.Log("✅ WebGL 템플릿 설정: Minimal");
        
        // Publishing Settings - Brotli 압축 및 WebAssembly 2023 타겟
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Brotli;
        PlayerSettings.WebGL.nameFilesAsHashes = false;  // 프로젝트명.data 등으로 파일명 설정
        PlayerSettings.WebGL.dataCaching = true;
        // Unity 6에서 debugSymbols -> debugSymbolMode로 변경
        PlayerSettings.WebGL.debugSymbolMode = WebGLDebugSymbolMode.Off;
        PlayerSettings.WebGL.showDiagnostics = false;
        PlayerSettings.WebGL.decompressionFallback = true;  // Decompression Fallback 활성화
        // WebAssembly 2023 타겟 설정 (Unity 6 - API가 변경되었을 수 있음)
        try
        {
            // Unity 6에서는 wasmDefines 속성이 없을 수 있음
            var wasmDefinesProp = typeof(PlayerSettings.WebGL).GetProperty("wasmDefines");
            if (wasmDefinesProp != null)
            {
                wasmDefinesProp.SetValue(null, "WEBGL2023");
                Debug.Log("✅ WebAssembly 2023 타겟 설정");
            }
            else
            {
                Debug.Log("ℹ️ WebAssembly 2023 설정 스킵 (Unity 6에서 자동 관리)");
            }
        }
        catch
        {
            Debug.Log("ℹ️ WebAssembly 2023 설정 스킵 (Unity 6에서 자동 관리)");
        }
        Debug.Log("✅ Publishing Settings: Brotli 압축 활성화, Decompression Fallback 활성화");
        
        // WebAssembly Language Features (이미지 기반)
        PlayerSettings.WebGL.exceptionSupport = WebGLExceptionSupport.ExplicitlyThrownExceptionsOnly;
        PlayerSettings.WebGL.threadsSupport = false;
        // Unity 6에서 wasmStreaming 제거됨 (decompressionFallback에 따라 자동 결정)
        Debug.Log("✅ WebAssembly 설정: 명시적 예외만, 멀티스레딩 비활성화, 스트리밍 자동");
        
        // Memory Settings (이미지 기반)
        PlayerSettings.WebGL.memorySize = 32;  // Initial Memory Size
        PlayerSettings.WebGL.memoryGrowthMode = WebGLMemoryGrowthMode.Geometric;
        PlayerSettings.WebGL.maximumMemorySize = 2048;
        Debug.Log("✅ 메모리 설정: 초기 32MB, 최대 2048MB, Geometric 증가");
        
        // Splash Screen 설정 (이미지 기반)
        PlayerSettings.SplashScreen.show = true;
        PlayerSettings.SplashScreen.showUnityLogo = false;
        PlayerSettings.SplashScreen.animationMode = PlayerSettings.SplashScreen.AnimationMode.Dolly;
        // Unity 6에서 logoAnimationMode 제거됨
        PlayerSettings.SplashScreen.overlayOpacity = 0.0f;
        PlayerSettings.SplashScreen.blurBackgroundImage = true;
        Debug.Log("✅ 스플래시 화면: Unity 로고 숨김, Dolly 애니메이션, 오버레이 투명");
        
        // WebGL 링커 타겟 설정 (Unity 6 최적화)
        PlayerSettings.WebGL.linkerTarget = WebGLLinkerTarget.Wasm;
        Debug.Log("✅ WebGL 링커 타겟 설정: WebAssembly (Unity 6 최적화)");
        
        // Code Optimization 설정 (Runtime Speed 또는 Runtime Speed with LTO)
        SetCodeOptimization();
        
        // Managed Stripping Level 설정 (Medium)
        try
        {
            // Unity 6에서는 StripEngineCode enum이 변경되었을 수 있음
            // 리플렉션을 사용하여 안전하게 설정
            var stripEngineCodeProp = typeof(PlayerSettings).GetProperty("stripEngineCode");
            if (stripEngineCodeProp != null)
            {
                var propType = stripEngineCodeProp.PropertyType;
                if (propType.IsEnum)
                {
                    // enum 타입인 경우
                    var enumValue = System.Enum.Parse(propType, "StripUnused");
                    stripEngineCodeProp.SetValue(null, enumValue);
                    Debug.Log("✅ Managed Stripping Level: Medium (StripUnused)");
                }
                else if (propType == typeof(int))
                {
                    // int 타입인 경우 (Unity 6)
                    stripEngineCodeProp.SetValue(null, 2);  // Medium = 2
                    Debug.Log("✅ Managed Stripping Level: Medium (Unity 6 방식, 값: 2)");
                }
            }
            else
            {
                Debug.LogWarning("⚠️ stripEngineCode 속성을 찾을 수 없습니다.");
            }
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("⚠️ Managed Stripping Level 설정 실패: " + e.Message);
            Debug.Log("ℹ️ Unity Editor에서 수동으로 설정해주세요.");
        }
        
        Debug.Log("🔧 WebGL Player Settings 이미지 기반 고정 설정 완료");
    }
    
    private static void SetCodeOptimization()
    {
        // Code Optimization 설정: Runtime Speed 또는 Runtime Speed with LTO
        try
        {
            #if UNITY_2021_3_OR_NEWER
            // Unity 2021.3 이상에서 시도
            var il2CppCodeGenType = typeof(Il2CppCodeGeneration);
            if (il2CppCodeGenType != null)
            {
                object enumValue;
                if (CODE_OPTIMIZATION_TYPE == "RuntimeSpeedWithLTO")
                {
                    // OptimizeForSize 또는 0 값 시도
                    try
                    {
                        enumValue = System.Enum.Parse(il2CppCodeGenType, "OptimizeForSize");
                    }
                    catch
                    {
                        // Unity 6에서는 enum 값이 다를 수 있음
                        enumValue = System.Enum.ToObject(il2CppCodeGenType, 0);
                    }
                    Debug.Log("✅ Code Optimization: Runtime Speed with LTO");
                }
                else
                {
                    // OptimizeForRuntime 또는 1 값 시도
                    try
                    {
                        enumValue = System.Enum.Parse(il2CppCodeGenType, "OptimizeForRuntime");
                    }
                    catch
                    {
                        // Unity 6에서는 enum 값이 다를 수 있음
                        enumValue = System.Enum.ToObject(il2CppCodeGenType, 1);
                    }
                    Debug.Log("✅ Code Optimization: Runtime Speed");
                }
                
                PlayerSettings.SetIl2CppCodeGeneration(NamedBuildTarget.WebGL, (Il2CppCodeGeneration)enumValue);
            }
            #endif
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("⚠️ Code Optimization 설정 실패: " + e.Message);
            Debug.Log("ℹ️ Unity Editor에서 수동으로 설정해주세요.");
        }
    }
    
    private static void LogCurrentPlayerSettings()
    {
        Debug.Log("=== 현재 WebGL Player Settings ===");
        Debug.Log("🎮 제품명: " + PlayerSettings.productName);
        Debug.Log("🏢 회사명: " + PlayerSettings.companyName);
        Debug.Log("📋 버전: " + PlayerSettings.bundleVersion);
        
        // Unity 6 호환성: 아이콘 API 확인 (Unity 버전에 따라 다름)
        try
        {
            // Unity 6에서는 NamedBuildTarget과 IconKind 사용
            var icons = PlayerSettings.GetIcons(NamedBuildTarget.WebGL, IconKind.Application);
            Debug.Log("🖼️ 기본 아이콘: " + (icons != null && icons.Length > 0 ? "설정됨" : "없음"));
        }
        catch
        {
            Debug.Log("🖼️ 기본 아이콘: 확인 불가 (Unity 버전 호환성 문제)");
        }
        
        // WebGL 전용 설정들
        Debug.Log("🌐 WebGL 템플릿: " + PlayerSettings.WebGL.template);
        Debug.Log("💾 WebGL 메모리 크기: " + PlayerSettings.WebGL.memorySize + "MB");
        Debug.Log("📦 WebGL 압축 포맷: " + PlayerSettings.WebGL.compressionFormat);
        Debug.Log("🔙 WebGL Decompression Fallback: " + PlayerSettings.WebGL.decompressionFallback);
        // WebAssembly 2023 확인 (Unity 6에서는 API가 변경되었을 수 있음)
        try
        {
            var wasmDefinesProp = typeof(PlayerSettings.WebGL).GetProperty("wasmDefines");
            if (wasmDefinesProp != null)
            {
                var wasmDefines = wasmDefinesProp.GetValue(null) as string;
                Debug.Log("🌐 WebGL WebAssembly 2023: " + (wasmDefines != null && wasmDefines.Contains("WEBGL2023") ? "활성화" : "비활성화"));
            }
            else
            {
                Debug.Log("🌐 WebGL WebAssembly 2023: Unity 6에서 자동 관리");
            }
        }
        catch
        {
            Debug.Log("🌐 WebGL WebAssembly 2023: 확인 불가");
        }
        Debug.Log("⚠️ WebGL 예외 지원: " + PlayerSettings.WebGL.exceptionSupport);
        Debug.Log("💽 WebGL 데이터 캐싱: " + PlayerSettings.WebGL.dataCaching);
        Debug.Log("📂 WebGL 파일명 방식: " + (PlayerSettings.WebGL.nameFilesAsHashes ? "해시" : "프로젝트명") + " 기반");
        Debug.Log("🔧 WebGL 링커 타겟: " + PlayerSettings.WebGL.linkerTarget);
        #if UNITY_2021_3_OR_NEWER
        try
        {
            var codeGen = PlayerSettings.GetIl2CppCodeGeneration(NamedBuildTarget.WebGL);
            Debug.Log("⚡ Code Optimization: " + codeGen);
            Debug.Log("📦 Managed Stripping Level: " + PlayerSettings.stripEngineCode);
        }
        catch (System.Exception e)
        {
            Debug.Log("⚡ Code Optimization: 확인 불가 (" + e.Message + ")");
        }
        #endif
        Debug.Log("🎯 WebGL 최적화: Unity 6에서 자동 관리");
        Debug.Log("=====================================");
    }
    
    private static BuildOptions GetBuildOptionsFromPlayerSettings()
    {
        BuildOptions options = BuildOptions.None;
        
        // Development Build 설정 확인
        if (EditorUserBuildSettings.development)
        {
            options |= BuildOptions.Development;
            Debug.Log("✅ Development Build 모드 활성화");
        }
        
        // Script Debugging 설정 확인
        if (EditorUserBuildSettings.allowDebugging)
        {
            options |= BuildOptions.AllowDebugging;
            Debug.Log("✅ Script Debugging 활성화");
        }
        
        // Profiler 설정 확인
        if (EditorUserBuildSettings.connectProfiler)
        {
            options |= BuildOptions.ConnectWithProfiler;
            Debug.Log("✅ Profiler 연결 활성화");
        }
        
        // Deep Profiling 설정 확인
        if (EditorUserBuildSettings.buildWithDeepProfilingSupport)
        {
            options |= BuildOptions.EnableDeepProfilingSupport;
            Debug.Log("✅ Deep Profiling 지원 활성화");
        }
        
        // Unity 6에서 autoRunPlayer 제거됨
        // WebGL은 브라우저에서 실행되므로 AutoRunPlayer 옵션 불필요
        Debug.Log("ℹ️ WebGL 빌드는 브라우저에서 수동 실행");
        
        return options;
    }
    
    private static void ApplyWebGLSettings()
    {
        Debug.Log("🌐 WebGL 특수 설정 적용 및 검증 중...");
        
        Debug.Log("🌐 WebGL 템플릿 사용: " + PlayerSettings.WebGL.template);
        Debug.Log("💾 WebGL 메모리 크기: " + PlayerSettings.WebGL.memorySize + "MB");
        Debug.Log("📦 WebGL 압축 포맷: " + PlayerSettings.WebGL.compressionFormat);
        Debug.Log("⚠️ WebGL 예외 지원: " + PlayerSettings.WebGL.exceptionSupport);
        Debug.Log("💽 WebGL 데이터 캐싱: " + PlayerSettings.WebGL.dataCaching);
        
        // WebGL 최적화 설정 확인 및 권장사항
        if (PlayerSettings.WebGL.memorySize < 256)
        {
            Debug.LogWarning("⚠️ WebGL 메모리 크기가 256MB 미만입니다. 과학실험 시뮬레이션에는 512MB 이상 권장합니다.");
        }
        else if (PlayerSettings.WebGL.memorySize >= 512)
        {
            Debug.Log("✅ WebGL 메모리 크기가 적절합니다 (512MB 이상).");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.WebGL.template) || PlayerSettings.WebGL.template == "APPLICATION:Default")
        {
            Debug.LogWarning("⚠️ WebGL 템플릿이 기본값입니다. 교육용 템플릿 사용을 권장합니다.");
        }
        else
        {
            Debug.Log("✅ WebGL 템플릿 설정됨: " + PlayerSettings.WebGL.template);
        }
        
        // WebGL 압축 설정 확인
        if (PlayerSettings.WebGL.compressionFormat == WebGLCompressionFormat.Disabled)
        {
            Debug.LogWarning("⚠️ WebGL 압축이 비활성화되어 있습니다. 파일 크기가 클 수 있습니다.");
        }
        else
        {
            Debug.Log("✅ WebGL 압축 활성화: " + PlayerSettings.WebGL.compressionFormat);
        }
        
        // Decompression Fallback 확인
        if (PlayerSettings.WebGL.decompressionFallback)
        {
            Debug.Log("✅ WebGL Decompression Fallback 활성화 (압축 해제 실패 시 대체 사용)");
        }
        
        // WebAssembly 2023 확인
        try
        {
            var wasmDefinesProp = typeof(PlayerSettings.WebGL).GetProperty("wasmDefines");
            if (wasmDefinesProp != null)
            {
                var wasmDefines = wasmDefinesProp.GetValue(null) as string;
                if (wasmDefines != null && wasmDefines.Contains("WEBGL2023"))
                {
                    Debug.Log("✅ WebAssembly 2023 타겟 활성화");
                }
            }
            else
            {
                Debug.Log("✅ WebAssembly 2023 타겟: Unity 6에서 자동 관리");
            }
        }
        catch
        {
            Debug.Log("ℹ️ WebAssembly 2023 확인 불가");
        }
        
        // Code Optimization 확인
        #if UNITY_2021_3_OR_NEWER
        try
        {
            var codeGen = PlayerSettings.GetIl2CppCodeGeneration(NamedBuildTarget.WebGL);
            string codeGenStr = codeGen.ToString();
            Debug.Log("✅ Code Optimization: " + codeGenStr + " (" + (CODE_OPTIMIZATION_TYPE == "RuntimeSpeedWithLTO" ? "Runtime Speed with LTO" : "Runtime Speed") + ")");
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("⚠️ Code Optimization 확인 불가: " + e.Message);
        }
        #endif
        
        // Managed Stripping Level 확인
        try
        {
            Debug.Log("✅ Managed Stripping Level: " + PlayerSettings.stripEngineCode + " (Medium)");
        }
        catch
        {
            Debug.Log("ℹ️ Managed Stripping Level 확인 불가");
        }
        
        // 과학실험 시뮬레이션에 최적화된 설정 권장사항
        Debug.Log("📚 과학실험 시뮬레이션 최적화 권장사항:");
        Debug.Log("  - 메모리: 512MB 이상");
        Debug.Log("  - 압축: Brotli (현재 설정됨)");
        Debug.Log("  - Decompression Fallback: 활성화 (현재 설정됨)");
        Debug.Log("  - WebAssembly 2023: 활성화 (현재 설정됨)");
        Debug.Log("  - Managed Stripping Level: Medium (현재 설정됨)");
        Debug.Log("  - 예외 지원: ExplicitlyThrownExceptionsOnly");
        Debug.Log("  - 데이터 캐싱: 활성화");
    }
    
    private static string[] GetBuildScenes()
    {
        // Build Settings에서 활성화된 씬들만 가져오기
        var enabledScenes = new System.Collections.Generic.List<string>();
        
        foreach (var scene in EditorBuildSettings.scenes)
        {
            if (scene.enabled)
            {
                enabledScenes.Add(scene.path);
            }
        }
        
        Debug.Log("📋 빌드할 씬 수: " + enabledScenes.Count);
        foreach (var scene in enabledScenes)
        {
            Debug.Log("  - " + scene);
        }
        
        return enabledScenes.ToArray();
    }
    
    private static string FormatBytes(ulong bytes)
    {
        string[] sizes = { "B", "KB", "MB", "GB", "TB" };
        double len = bytes;
        int order = 0;
        while (len >= 1024 && order < sizes.Length - 1)
        {
            order++;
            len = len / 1024;
        }
        return len.ToString("0.##") + " " + sizes[order];
    }
}
""")
    
    try:
        formatted_content = script_template.substitute(
            output_path=output_path_formatted,
            code_optimization=code_optimization
        )
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        print(f"WebGL 전용 빌드 스크립트 생성 완료: {script_path}")
        print(f"  ⚡ Code Optimization: {code_optimization}")
        return True
    except Exception as e:
        print(f"WebGL 빌드 스크립트 생성 실패: {e}")
        return False

def run_unity_webgl_build(project_path, timeout=BUILD_TIMEOUT):
    """Unity CLI를 사용하여 WebGL 빌드를 실행합니다. (Player Settings 완전 반영)"""
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
    
    print(f"🌐 Unity WebGL Player Settings 반영 빌드 시작: {project_name}")
    
    # 빌드 출력 디렉토리 미리 생성
    project_build_dir = os.path.join(BUILD_OUTPUT_DIR, project_name)
    
    # 로그 파일 경로 생성
    log_dir = os.path.join(BUILD_OUTPUT_DIR, "_Logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"{project_name}_{timestamp}.log")
    
    try:
        if not os.path.exists(project_build_dir):
            os.makedirs(project_build_dir, exist_ok=True)
            print(f"빌드 출력 디렉토리 생성: {project_build_dir}")
        else:
            print(f"빌드 출력 디렉토리 확인 완료: {project_build_dir}")
    except Exception as e:
        print(f"빌드 출력 디렉토리 생성 실패: {e}")
        return False
    
    # WebGL 전용 빌드 스크립트 생성
    if not create_unity_webgl_build_script(project_path):
        return False
    
    # Unity CLI 명령어 구성
    cmd = [
        unity_path,
        "-batchmode",
        "-quit", 
        "-projectPath", project_path,
        "-buildTarget", "WebGL",
        "-executeMethod", "AutoWebGLBuildScript.BuildWebGLWithPlayerSettings",
        "-logFile", log_file_path  # 로그 파일 경로 지정
    ]
    
    print(f"📝 로그 파일 경로: {log_file_path}")
    
    try:
        print(f"🌐 Unity WebGL 빌드 실행 중... (타임아웃: {timeout}초)")
        print(f"명령어: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            timeout=timeout,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 로그 파일에 stdout과 stderr 추가 저장
        try:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write("\n" + "="*80 + "\n")
                log_file.write("Python Script Output (stdout/stderr)\n")
                log_file.write("="*80 + "\n")
                log_file.write(f"Return Code: {result.returncode}\n")
                log_file.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                if result.stdout:
                    log_file.write("\n--- STDOUT ---\n")
                    log_file.write(result.stdout)
                if result.stderr:
                    log_file.write("\n--- STDERR ---\n")
                    log_file.write(result.stderr)
                log_file.write("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"⚠️ 로그 파일 추가 저장 실패: {e}")
        
        # 로그 출력
        if result.stdout:
            print("=== Unity WebGL 빌드 로그 ===")
            print(result.stdout)
        
        if result.stderr:
            print("=== Unity WebGL 빌드 에러 ===")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Unity WebGL 빌드 성공: {project_name}")
            if os.path.exists(log_file_path):
                print(f"📝 빌드 로그: {log_file_path}")
            return True
        else:
            print(f"❌ Unity WebGL 빌드 실패: {project_name} (종료 코드: {result.returncode})")
            
            # 오류 발생 시 로그 파일의 마지막 부분 읽어서 표시
            try:
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                        log_lines = log_file.readlines()
                        if log_lines:
                            print("\n" + "="*80)
                            print("📝 로그 파일 마지막 50줄 (오류 확인):")
                            print("="*80)
                            last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                            for line in last_lines:
                                print(line.rstrip())
                            print("="*80)
            except Exception as e:
                print(f"⚠️ 로그 파일 읽기 실패: {e}")
            
            if os.path.exists(log_file_path):
                print(f"📝 전체 실패 로그: {log_file_path}")
            return False
            
    except subprocess.TimeoutExpired:
        error_msg = f"Unity WebGL 빌드 타임아웃: {project_name} ({timeout}초 초과)"
        print(f"❌ {error_msg}")
        
        # 타임아웃 오류를 로그 파일에 추가 저장
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write("\n" + "="*80 + "\n")
                    log_file.write(f"TIMEOUT ERROR: {error_msg}\n")
                    log_file.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write("="*80 + "\n")
                
                # 로그 파일의 마지막 부분 표시
                with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                    log_lines = log_file.readlines()
                    if log_lines:
                        print("\n" + "="*80)
                        print("📝 타임아웃 직전 로그 (마지막 50줄):")
                        print("="*80)
                        last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                        for line in last_lines:
                            print(line.rstrip())
                        print("="*80)
        except Exception as e:
            print(f"⚠️ 타임아웃 로그 저장 실패: {e}")
        
        if os.path.exists(log_file_path):
            print(f"📝 전체 타임아웃 로그: {log_file_path}")
        return False
        
    except Exception as e:
        error_msg = f"Unity WebGL 빌드 예외: {project_name} - {e}"
        print(f"❌ {error_msg}")
        
        # 예외 오류를 로그 파일에 추가 저장
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write("\n" + "="*80 + "\n")
                    log_file.write(f"EXCEPTION ERROR: {error_msg}\n")
                    log_file.write(f"Exception Type: {type(e).__name__}\n")
                    log_file.write(f"Exception Details: {str(e)}\n")
                    import traceback
                    log_file.write("\n--- Traceback ---\n")
                    log_file.write(traceback.format_exc())
                    log_file.write(f"\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write("="*80 + "\n")
                
                # 로그 파일의 마지막 부분 표시
                with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                    log_lines = log_file.readlines()
                    if log_lines:
                        print("\n" + "="*80)
                        print("📝 예외 발생 직전 로그 (마지막 50줄):")
                        print("="*80)
                        last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                        for line in last_lines:
                            print(line.rstrip())
                        print("="*80)
        except Exception as log_error:
            print(f"⚠️ 예외 로그 저장 실패: {log_error}")
        
        if os.path.exists(log_file_path):
            print(f"📝 전체 예외 로그: {log_file_path}")
        return False

def build_multiple_webgl_projects(project_dirs, parallel=False, max_workers=2):
    """여러 Unity 프로젝트를 WebGL로 빌드합니다."""
    print(f"\n=== Unity WebGL 다중 프로젝트 빌드 시작 ===")
    
    if parallel:
        return build_multiple_webgl_projects_parallel(project_dirs, max_workers)
    else:
        return build_multiple_webgl_projects_sequential(project_dirs)

def build_multiple_webgl_projects_sequential(project_dirs):
    """여러 Unity 프로젝트를 WebGL로 순차적으로 빌드합니다."""
    success_count = 0
    fail_count = 0
    results = []
    
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            print(f"❌ 프로젝트 경로가 존재하지 않습니다: {project_dir}")
            fail_count += 1
            results.append((get_project_name_from_path(project_dir), False))
            continue
        
        project_name = get_project_name_from_path(project_dir)
        print(f"\n--- {project_name} WebGL 빌드 시작 ---")
        
        if run_unity_webgl_build(project_dir):
            success_count += 1
            results.append((project_name, True))
        else:
            fail_count += 1
            results.append((project_name, False))
    
    print(f"\n=== WebGL 순차 빌드 결과 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 빌드: {success_count + fail_count}개")
    
    return results

def build_multiple_webgl_projects_parallel(project_dirs, max_workers=2):
    """여러 Unity 프로젝트를 WebGL로 병렬로 빌드합니다."""
    print(f"🌐 WebGL 병렬 빌드 시작 (최대 {max_workers}개 동시 실행)")
    
    success_count = 0
    fail_count = 0
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 모든 프로젝트를 병렬로 제출
        future_to_project = {
            executor.submit(run_unity_webgl_build, project_dir): project_dir 
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
                    print(f"✅ {project_name} WebGL 병렬 빌드 완료")
                else:
                    fail_count += 1
                    print(f"❌ {project_name} WebGL 병렬 빌드 실패")
                results.append((project_name, result))
            except Exception as e:
                fail_count += 1
                print(f"❌ {project_name} WebGL 병렬 빌드 예외: {e}")
                results.append((project_name, False))
    
    print(f"\n=== WebGL 병렬 빌드 결과 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 빌드: {success_count + fail_count}개")
    
    return results

def clean_build_outputs(project_dirs):
    """중앙 집중식 빌드 출력물을 정리합니다."""
    print("\n=== 중앙 집중식 빌드 출력물 정리 시작 ===")
    print(f"📁 중앙 빌드 폴더: {BUILD_OUTPUT_DIR}")
    
    if not os.path.exists(BUILD_OUTPUT_DIR):
        print("⚪ 중앙 빌드 폴더가 존재하지 않습니다.")
        return
    
    cleaned_count = 0
    total_size = 0
    
    # 각 프로젝트별 빌드 폴더 정리
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            continue
            
        project_name = get_project_name_from_path(project_dir)
        project_build_dir = os.path.join(BUILD_OUTPUT_DIR, project_name)
        
        if os.path.exists(project_build_dir):
            try:
                import shutil
                # 폴더 크기 계산
                folder_size = 0
                for dirpath, dirnames, filenames in os.walk(project_build_dir):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            folder_size += os.path.getsize(filepath)
                        except:
                            pass
                
                total_size += folder_size
                shutil.rmtree(project_build_dir)
                
                # 크기를 읽기 쉬운 형태로 변환
                size_str = format_bytes(folder_size)
                print(f"✅ {project_name} 중앙 빌드 출력물 정리 완료 ({size_str})")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ {project_name} 중앙 빌드 출력물 정리 실패: {e}")
        else:
            print(f"⚪ {project_name} 중앙 빌드 출력물 없음")
    
    total_size_str = format_bytes(total_size)
    print(f"\n📊 정리 완료: {cleaned_count}개 프로젝트, 총 {total_size_str} 절약")
    print(f"📁 중앙 빌드 폴더: {BUILD_OUTPUT_DIR}")

def format_bytes(bytes_size):
    """바이트 크기를 읽기 쉬운 형태로 변환합니다."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"
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
    print("  --package-only   패키지 추가만 실행 (Git 작업 제외)")
    print("  --git-push       Git 커밋 및 푸시만 실행 (패키지 추가 제외)")
    print("  --git-commit     Git 커밋만 실행 (푸시 제외)")
    print("  --unity-batch    Unity 배치 모드로 Editor 스크립트 실행 (40개 프로젝트 자동화)")
    print("  --parallel       Unity 배치 모드를 병렬로 실행 (빠른 처리, 메모리 사용량 증가)")
    print("  --build-webgl    Unity WebGL 빌드 자동화 (Player Settings 완전 반영)")
    print("  --build-parallel WebGL 빌드를 병렬로 실행 (2개씩 동시 빌드)")
    print("  --build-only     WebGL 빌드만 실행 (Git 작업 및 패키지 추가 제외)")
    print("  --clean-builds   중앙 집중식 빌드 출력물 정리 (프로젝트별 폴더 삭제)")

    print("  --add-system-methods SystemManager에 공통 메소드 추가 (AllowKeyboardInput 등)")
    print("  --add-hello-world    SystemManager에 Hello World 메소드 추가 및 Start() 호출 설정")
    print("")
    print("기본 동작:")
    print("1. Unity 패키지 추가만 실행 (Git 작업 분리)")
    print("")
    print("Git 작업 (별도 실행):")
    print("  --git-push       모든 프로젝트에 Git 커밋 및 푸시 실행")
    print("  --git-commit     모든 프로젝트에 Git 커밋만 실행 (푸시 제외)")
    print("")
    print("Unity 배치 모드 (--unity-batch):")
    print("- Unity Editor를 배치 모드로 실행하여 Editor 스크립트 자동 실행")
    print("- 패키지 임포트 및 프로젝트 설정 검증 수행")
    print("- 40개 프로젝트를 순차적으로 자동 처리 (기본)")
    print("- --parallel 옵션으로 병렬 처리 가능 (3개씩 동시 실행)")
    print("- Unity GUI 없이 백그라운드에서 실행")
    print("- Git 작업과 독립적으로 실행 (자동 커밋/푸시 없음)")
    print("")
    print("Unity WebGL 중앙 집중식 빌드 자동화 (--build-webgl):")
    print("- Unity CLI를 사용하여 WebGL 프로젝트를 중앙 집중식으로 자동 빌드")
    print("- Player Settings 완전 반영 (제품명, 회사명, 버전, WebGL 설정 등)")
    print("- Build Settings의 활성화된 씬만 빌드")
    print("- Development Build, Profiler 등 빌드 옵션 자동 적용")
    print("- WebGL 전용 최적화 설정 적용 (메모리, 압축, 템플릿 등)")
    print("- 프로젝트명 기반 파일명 생성 (프로젝트명.data, 프로젝트명.wasm 등)")
    print("- 과학실험 시뮬레이션에 최적화된 WebGL 빌드")
    print(f"- 중앙 빌드 출력: {BUILD_OUTPUT_DIR}\\프로젝트명\\ 폴더")
    print("- --build-parallel로 병렬 빌드 가능 (2개씩 동시 빌드)")
    print("- 빌드 시간: 프로젝트당 5-15분 (WebGL 최적화 포함)")
    print("- 하나의 폴더에서 모든 프로젝트 빌드 결과 통합 관리")
    print("")
    print("WebGL 빌드 전용 모드 (--build-only):")
    print("- Git 작업(커밋, 푸시, 브랜치 변경) 완전 제외")
    print("- 패키지 추가 작업 제외")
    print("- 오직 WebGL 빌드만 수행 (순수 빌드 모드)")
    print("- 기존 프로젝트 상태 그대로 유지하면서 빌드")
    print("- 빌드 결과만 필요한 경우 최적화된 옵션")
    print("- --build-parallel과 함께 사용 가능")
    print("")
    print("SystemManager 메소드 추가 (--add-system-methods):")
    print("- 모든 프로젝트의 SystemManager.cs 파일을 자동 탐색")
    print("- 클래스의 마지막 부분(닫는 중괄호 직전)에 메소드 추가")
    print("- 기본 메소드: AllowKeyboardInput (WebGL 키보드 입력 제어)")
    print("- 같은 이름의 메소드가 이미 존재하면 자동 생략")
    print("- 다른 메소드도 SYSTEM_MANAGER_METHODS 딕셔너리에 추가하여 사용 가능")
    print("- 사용자 정의 메소드는 add_custom_method_to_system_managers() 함수 사용")
    print("- 변경사항이 있으면 자동으로 Git 커밋 (푸시 제외)")
    print("")
    print("SystemManager Hello World 메소드 추가 (--add-hello-world):")
    print("- 모든 프로젝트의 SystemManager.cs 파일을 자동 탐색")
    print("- 클래스의 제일 아래에 private void PrintHelloWorld() 메소드 추가")
    print("- 기존 Start() 함수의 가장 아래에 PrintHelloWorld() 호출 추가")
    print("- Debug.Log(\"Hello World!\") 로그 출력")
    print("- 이미 메소드가 존재하거나 호출이 있으면 자동 생략")
    print("- 들여쓰기 패턴 자동 분석하여 코드 스타일 유지")
    print("- 변경사항이 있으면 자동으로 Git 커밋 (푸시 제외)")
    print("")
    print("Git 브랜치 전략:")
    print("- 브랜치 계층구조에서 가장 깊은(아래) 브랜치를 우선 사용")
    print("- 커밋 수가 많고 최근에 작업된 브랜치 선택")
    print("- 적절한 브랜치가 없으면 dev 브랜치 사용/생성")
    print("")
    print("Git 작업 분리 시스템:")
    print("- 패키지 추가와 Git 커밋/푸시를 독립적으로 실행 가능")
    print("- 빌드 작업 시 Git 작업 자동 실행 방지")
    print("- 필요에 따라 커밋만 하거나 푸시까지 선택 가능")
    print("- 각 작업의 실행 시점을 개발자가 직접 제어")
    print("=====================================")

def main():
    """메인 실행 함수"""
    # 도움말 요청 확인
    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        return
    
    print("=== Unity 프로젝트 자동화 도구 시작 ===\n")
    
    # 명령행 인수 확인
    package_only = "--package-only" in sys.argv
    git_push = "--git-push" in sys.argv
    git_commit = "--git-commit" in sys.argv
    unity_batch = "--unity-batch" in sys.argv
    parallel = "--parallel" in sys.argv
    build_webgl = "--build-webgl" in sys.argv
    build_parallel = "--build-parallel" in sys.argv
    build_only = "--build-only" in sys.argv
    clean_builds = "--clean-builds" in sys.argv

    add_system_methods = "--add-system-methods" in sys.argv
    add_hello_world = "--add-hello-world" in sys.argv
    
    # 옵션에 따른 모드 설정
    if build_only:
        print("WebGL 빌드만 실행합니다 (Git 작업 및 패키지 추가 제외)...\n")
        build_webgl = True
    elif package_only:
        print("패키지 추가만 실행합니다 (Git 작업 제외)...\n")
    elif git_push:
        print("Git 커밋 및 푸시만 실행합니다 (패키지 추가 제외)...\n")
    elif git_commit:
        print("Git 커밋만 실행합니다 (푸시 제외)...\n")
    elif unity_batch:
        print("Unity 배치 모드만 실행합니다...\n")
    elif clean_builds:
        print("빌드 출력물 정리만 실행합니다...\n")
    elif not (add_system_methods or add_hello_world):
        print("기본 모드: 패키지 추가만 실행합니다...\n")
    
    # SystemManager 메소드 추가만 실행하는 경우
    if add_system_methods:
        print("SystemManager 메소드 추가 시작...")
        methods_added = add_methods_to_system_managers(project_dirs)
        
        # 변경사항이 있으면 Git 커밋만 (푸시 제외)
        if methods_added:
            print("\n메소드가 추가되어 Git 커밋을 진행합니다 (푸시 제외)...")
            for project_dir in project_dirs:
                if os.path.exists(project_dir):
                    commit_changes(project_dir, "system_manager_update")
        else:
            print("변경사항이 없어 Git 커밋을 생략합니다.")
        return
    
    # SystemManager Hello World 메소드 추가만 실행하는 경우
    if add_hello_world:
        print("SystemManager Hello World 메소드 추가 시작...")
        hello_world_added = add_hello_world_to_all_system_managers(project_dirs)
        
        # 변경사항이 있으면 Git 커밋만 (푸시 제외)
        if hello_world_added:
            print("\nHello World 메소드가 추가되어 Git 커밋을 진행합니다 (푸시 제외)...")
            for project_dir in project_dirs:
                if os.path.exists(project_dir):
                    commit_changes(project_dir, "system_manager_update", "FEAT: SystemManager에 Hello World 메소드 추가 및 Start() 호출 설정")
        else:
            print("변경사항이 없어 Git 커밋을 생략합니다.")
        return
    
    # 패키지 추가 (git_push나 git_commit이 아닌 경우에만 실행)
    if not git_push and not git_commit and not build_only and not unity_batch and not clean_builds:
        print("1. Unity 패키지 추가 작업 시작...")
        for project_dir in project_dirs:
            project_name = get_project_name_from_path(project_dir)
            print(f"\n--- {project_name} 패키지 추가 ---")
            add_git_packages_to_manifest(project_dir, git_packages)

    # Git 커밋 및 푸시 (git_push인 경우에만 실행)
    if git_push:
        print("\n2. Git 커밋 및 푸시 작업 시작...")
        
        commit_message_type = "package_update"
        print(f"📝 커밋 메시지 타입: {commit_message_type}")
        
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                commit_and_push_changes(project_dir, commit_message_type)
            else:
                print(f"프로젝트 폴더 없음: {project_dir}")
    
    # Git 커밋만 (git_commit인 경우에만 실행)
    if git_commit:
        print("\n2. Git 커밋 작업 시작 (푸시 제외)...")
        
        commit_message_type = "package_update"
        print(f"📝 커밋 메시지 타입: {commit_message_type}")
        
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                commit_changes(project_dir, commit_message_type)
            else:
                print(f"프로젝트 폴더 없음: {project_dir}")

    # Unity 배치 모드 실행 (unity-batch인 경우에만 실행)
    if unity_batch:
        print("\n3. Unity 배치 모드 실행 시작...")
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
    
    # 빌드 출력물 정리 (clean-builds인 경우에만 실행)
    if clean_builds:
        print("\n4. 빌드 출력물 정리 시작...")
        clean_build_outputs(project_dirs)
    
    # Unity WebGL 프로젝트 빌드 (build-webgl인 경우에만 실행)
    if build_webgl:
        print(f"\n5. Unity WebGL 프로젝트 빌드 시작...")
        
        print(f"🌐 빌드 타겟: WebGL")
        print(f"📊 총 {len(project_dirs)}개 프로젝트 빌드 예정")
        print("🎯 WebGL Player Settings 완전 반영 빌드 모드")
        print("📚 과학실험 시뮬레이션 최적화 적용")
        
        # WebGL 빌드 실행
        build_results = build_multiple_webgl_projects(
            project_dirs, 
            parallel=build_parallel,
            max_workers=2 if build_parallel else 1
        )
        
        # 빌드 결과 요약
        success_builds = sum(1 for _, success in build_results if success)
        fail_builds = len(build_results) - success_builds
        
        print(f"\n=== 최종 WebGL 빌드 결과 ===")
        print(f"✅ 성공: {success_builds}개")
        print(f"❌ 실패: {fail_builds}개")
        print(f"📊 총 빌드: {len(build_results)}개")
        
        if success_builds > 0:
            print(f"\n🌐 WebGL 빌드 완료된 프로젝트들:")
            for project_name, success in build_results:
                if success:
                    print(f"  - {project_name}")
        
        if fail_builds > 0:
            print(f"\n❌ WebGL 빌드 실패한 프로젝트들:")
            for project_name, success in build_results:
                if not success:
                    print(f"  - {project_name}")
    
    print("\n=== 모든 작업 완료 ===")

if __name__ == "__main__":
    main()

# endregion 