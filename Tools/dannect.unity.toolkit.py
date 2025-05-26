import os
import json
import chardet
import subprocess
import sys

# =========================
# #region 프로젝트 폴더 및 패키지 정보 (최상단에 위치)
# =========================
project_dirs = [
    r"E:\TDS",

    
    # ... 필요시 추가
]

git_packages = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    # 필요시 추가
}

# Git 설정
GIT_BASE_URL = "https://github.com/Dannect/"
DEFAULT_BRANCH = "main"
DEV_BRANCH = "dev"
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
    print("  --help        이 도움말을 표시합니다")
    print("  --skip-git    Git 작업을 건너뜁니다 (UTF-8 변환과 패키지 추가만 실행)")
    print("  --git-only    Git 작업만 실행합니다 (UTF-8 변환과 패키지 추가 건너뜀)")
    print("")
    print("기본 동작:")
    print("1. C# 파일 UTF-8 변환")
    print("2. Unity 패키지 추가")
    print("3. Git 커밋 및 푸시 (계층구조 최하위 브랜치 또는 dev 브랜치)")
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
    
    if git_only:
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
    
    print("\n=== 모든 작업 완료 ===")

if __name__ == "__main__":
    main()

# endregion 