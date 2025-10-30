"""
Git 관련 유틸리티 함수들
"""
import os
import subprocess
from config import Config


# 전역 변수 참조 (호환성 유지)
GIT_BASE_URL = Config.GIT_BASE_URL
DEFAULT_BRANCH = Config.DEFAULT_BRANCH
DEV_BRANCH = Config.DEV_BRANCH
COMMIT_MESSAGES = Config.COMMIT_MESSAGES


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

