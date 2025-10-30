"""
메인 실행부 및 CLI 인터페이스
"""
import os
import sys
from config import Config, WEBGL_CODE_OPTIMIZATION
from git_utils import commit_changes, commit_and_push_changes, get_project_name_from_path
from package_manager import add_git_packages_to_manifest
from unity_cli import create_unity_batch_script, process_multiple_projects_parallel, process_unity_project_batch
from system_manager import add_methods_to_system_managers, add_hello_world_to_all_system_managers
from build_manager import build_multiple_webgl_projects, clean_build_outputs

# 전역 변수 참조 (호환성 유지)
project_dirs = Config.PROJECT_DIRS
git_packages = Config.GIT_PACKAGES
BUILD_OUTPUT_DIR = Config.BUILD_OUTPUT_DIR

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
    print("  --build-parallel WebGL 빌드를 병렬로 실행 (기본: 4개씩 동시 빌드)")
    print("  --max-workers N  병렬 빌드 작업자 수 지정 (기본: 4, 권장: 3-5)")
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
    print(f"- Code Optimization: {Config.WEBGL_CODE_OPTIMIZATION}")
    print("  (옵션: BuildTimes, RuntimeSpeed, RuntimeSpeedLTO, DiskSize, DiskSizeLTO)")
    print(f"- 중앙 빌드 출력: {BUILD_OUTPUT_DIR}\\프로젝트명\\ 폴더")
    print("- --build-parallel로 병렬 빌드 가능 (기본: 4개씩 동시 빌드)")
    print("- --max-workers N으로 병렬 작업자 수 조절 가능 (권장: 3-5)")
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
    
    # max_workers 파싱 (기본값: 4)
    max_workers = 4
    for i, arg in enumerate(sys.argv):
        if arg == "--max-workers" and i + 1 < len(sys.argv):
            try:
                max_workers = int(sys.argv[i + 1])
                if max_workers < 1:
                    print("⚠️ max_workers는 1 이상이어야 합니다. 기본값 4 사용")
                    max_workers = 4
                elif max_workers > 8:
                    print("⚠️ max_workers가 8을 초과하면 시스템 리소스 부족 위험. 8로 제한")
                    max_workers = 8
            except ValueError:
                print("⚠️ max_workers 값이 유효하지 않습니다. 기본값 4 사용")
                max_workers = 4
    
    # 옵션에 따른 모드 설정
    if build_only:
        print("📦 WebGL 빌드만 실행합니다 (Git 작업 및 패키지 추가 제외)\n")
        build_webgl = True
    elif package_only:
        print("📦 패키지 추가만 실행합니다 (Git 작업 제외)\n")
    elif git_push:
        print("🔀 Git 커밋 및 푸시만 실행합니다 (패키지 추가 제외)\n")
    elif git_commit:
        print("💾 Git 커밋만 실행합니다 (푸시 제외)\n")
    elif unity_batch:
        print("⚙️ Unity 배치 모드만 실행합니다\n")
    elif clean_builds:
        print("🧹 빌드 출력물 정리만 실행합니다\n")
    elif not (add_system_methods or add_hello_world):
        print("📦 기본 모드: 패키지 추가만 실행합니다\n")
    
    # SystemManager 메소드 추가만 실행하는 경우
    if add_system_methods:
        print("🔧 SystemManager 메소드 추가 작업 시작...")
        methods_added = add_methods_to_system_managers(project_dirs)
        
        # 변경사항이 있으면 Git 커밋만 (푸시 제외)
        if methods_added:
            print("\n💾 변경사항이 있어 Git 커밋을 진행합니다 (푸시 제외)")
            for project_dir in project_dirs:
                if os.path.exists(project_dir):
                    commit_changes(project_dir, "system_manager_update")
        else:
            print("ℹ️ 변경사항이 없어 Git 커밋을 생략합니다")
        return
    
    # SystemManager Hello World 메소드 추가만 실행하는 경우
    if add_hello_world:
        print("👋 SystemManager Hello World 메소드 추가 작업 시작...")
        hello_world_added = add_hello_world_to_all_system_managers(project_dirs)
        
        # 변경사항이 있으면 Git 커밋만 (푸시 제외)
        if hello_world_added:
            print("\n💾 변경사항이 있어 Git 커밋을 진행합니다 (푸시 제외)")
            for project_dir in project_dirs:
                if os.path.exists(project_dir):
                    commit_changes(project_dir, "system_manager_update", "FEAT: SystemManager에 Hello World 메소드 추가 및 Start() 호출 설정")
        else:
            print("ℹ️ 변경사항이 없어 Git 커밋을 생략합니다")
        return
    
    # 패키지 추가 (git_push나 git_commit이 아닌 경우에만 실행)
    if not git_push and not git_commit and not build_only and not unity_batch and not clean_builds:
        print("\n📦 Unity 패키지 추가 작업 시작...")
        for project_dir in project_dirs:
            project_name = get_project_name_from_path(project_dir)
            print(f"\n📦 {project_name} 패키지 추가 중...")
            add_git_packages_to_manifest(project_dir, git_packages)

    # Git 커밋 및 푸시 (git_push인 경우에만 실행)
    if git_push:
        print("\n🔀 Git 커밋 및 푸시 작업 시작...")
        
        commit_message_type = "package_update"
        print(f"📝 커밋 메시지 타입: {commit_message_type}")
        
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                commit_and_push_changes(project_dir, commit_message_type)
            else:
                print(f"⚠️ 프로젝트 폴더 없음: {project_dir}")
    
    # Git 커밋만 (git_commit인 경우에만 실행)
    if git_commit:
        print("\n💾 Git 커밋 작업 시작 (푸시 제외)...")
        
        commit_message_type = "package_update"
        print(f"📝 커밋 메시지 타입: {commit_message_type}")
        
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                commit_changes(project_dir, commit_message_type)
            else:
                print(f"⚠️ 프로젝트 폴더 없음: {project_dir}")

    # Unity 배치 모드 실행 (unity-batch인 경우에만 실행)
    if unity_batch:
        print("\n⚙️ Unity 배치 모드 실행 시작...")
        print(f"📊 총 {len(project_dirs)}개 프로젝트 처리 예정")
        
        # 모든 프로젝트에 배치 스크립트 생성
        print("📝 배치 스크립트 생성 중...")
        for project_dir in project_dirs:
            if os.path.exists(project_dir):
                create_unity_batch_script(project_dir)
        
        if parallel:
            # 병렬 처리
            print("⚡ 병렬 처리 모드로 실행합니다 (최대 3개 동시 실행)")
            process_multiple_projects_parallel(project_dirs, max_workers=3)
        else:
            # 순차 처리 (기본)
            print("📋 순차 처리 모드로 실행합니다")
            success_count = 0
            fail_count = 0
            
            for i, project_dir in enumerate(project_dirs, 1):
                project_name = get_project_name_from_path(project_dir)
                print(f"\n[{i}/{len(project_dirs)}] {project_name} 처리 중...")
                
                if not os.path.exists(project_dir):
                    print(f"⚠️ 프로젝트 폴더 없음: {project_dir}")
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
            print(f"✅ 성공: {success_count}개")
            print(f"❌ 실패: {fail_count}개")
            print(f"📊 총 처리: {success_count + fail_count}개")
    
    # 빌드 출력물 정리 (clean-builds인 경우에만 실행)
    if clean_builds:
        print("\n🧹 빌드 출력물 정리 작업 시작...")
        clean_build_outputs(project_dirs)
    
    # Unity WebGL 프로젝트 빌드 (build-webgl인 경우에만 실행)
    if build_webgl:
        print(f"\n🌐 Unity WebGL 프로젝트 빌드 시작...")
        print(f"📊 총 {len(project_dirs)}개 프로젝트 빌드 예정")
        
        # 병렬 빌드 설정 표시
        if build_parallel:
            print(f"⚡ 병렬 빌드 모드: {max_workers}개 동시 실행")
        else:
            print(f"📋 순차 빌드 모드")
        
        # Code Optimization 설정 표시
        if WEBGL_CODE_OPTIMIZATION == "RuntimeSpeedLTO":
            print(f"⚡ Code Optimization: Runtime Speed with LTO (최고 성능, LTO 적용)")
        elif WEBGL_CODE_OPTIMIZATION == "RuntimeSpeed":
            print(f"⚡ Code Optimization: Runtime Speed (성능 최적화)")
        elif WEBGL_CODE_OPTIMIZATION == "BuildTimes":
            print(f"⚡ Code Optimization: Build Times (빠른 빌드)")
        elif WEBGL_CODE_OPTIMIZATION == "DiskSize":
            print(f"⚡ Code Optimization: Disk Size (크기 최적화)")
        elif WEBGL_CODE_OPTIMIZATION == "DiskSizeLTO":
            print(f"⚡ Code Optimization: Disk Size with LTO (최소 크기, LTO 적용)")
        else:
            print(f"⚡ Code Optimization: {WEBGL_CODE_OPTIMIZATION}")
        
        # WebGL 빌드 실행
        build_results = build_multiple_webgl_projects(
            project_dirs, 
            parallel=build_parallel,
            max_workers=max_workers if build_parallel else 1
        )
        
        # 빌드 결과 요약
        success_builds = sum(1 for _, success, _ in build_results if success)
        fail_builds = len(build_results) - success_builds
        
        # 전체 빌드 시간 계산
        total_build_time = sum(elapsed_time for _, _, elapsed_time in build_results)
        total_minutes = int(total_build_time // 60)
        total_seconds = int(total_build_time % 60)
        total_time_str = f"{total_minutes}분 {total_seconds}초" if total_minutes > 0 else f"{total_seconds}초"
        
        print(f"\n=== 최종 WebGL 빌드 결과 ===")
        print(f"✅ 성공: {success_builds}개")
        print(f"❌ 실패: {fail_builds}개")
        print(f"📊 총 빌드: {len(build_results)}개")
        print(f"⏱️ 전체 빌드 소요 시간: {total_time_str}")
        
        if success_builds > 0:
            print(f"\n✅ WebGL 빌드 완료된 프로젝트:")
            for project_name, success, elapsed_time in build_results:
                if success:
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
                    print(f"  • {project_name} - {time_str}")
        
        if fail_builds > 0:
            print(f"\n❌ WebGL 빌드 실패한 프로젝트:")
            for project_name, success, elapsed_time in build_results:
                if not success:
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
                    print(f"  • {project_name} - {time_str}")
    
    print("\n✨ 모든 작업 완료")

if __name__ == "__main__":
    main()

# endregion 