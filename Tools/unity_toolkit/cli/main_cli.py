"""
Unity 툴킷 명령줄 인터페이스

기존의 복잡한 명령줄 처리를 구조화하고 개선한 CLI 모듈입니다.
"""

import sys
import argparse
from typing import List
from ..unity_toolkit import UnityToolkit
from ..config.settings import DEFAULT_PROJECT_PATHS, DEFAULT_GIT_PACKAGES


def create_argument_parser() -> argparse.ArgumentParser:
    """명령줄 인수 파서를 생성합니다."""
    parser = argparse.ArgumentParser(
        description="Unity 프로젝트 자동화 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python -m unity_toolkit                    # 기본 자동화 워크플로우
  python -m unity_toolkit --full-auto       # 전체 자동화 (Unity 배치 포함)
  python -m unity_toolkit --build-webgl     # WebGL 빌드만 실행
  python -m unity_toolkit --maintenance     # 유지보수 워크플로우
  python -m unity_toolkit --projects "C:\\Project1" "C:\\Project2"  # 특정 프로젝트만

워크플로우 설명:
  기본 워크플로우: UTF-8 변환 → Unity 6 API 수정 → 패키지 업데이트 → Git 커밋
  전체 자동화: 기본 워크플로우 + Unity 배치 모드 실행
  빌드 워크플로우: WebGL 빌드 자동화 (Player Settings 완전 반영)
  유지보수: 프로젝트 검증, 호환성 검사, Git 상태 확인
        """
    )
    
    # 기본 옵션들
    parser.add_argument(
        '--projects', 
        nargs='*', 
        help='처리할 Unity 프로젝트 경로들 (기본값: 설정 파일의 프로젝트들)'
    )
    
    parser.add_argument(
        '--parallel', 
        action='store_true', 
        help='병렬 처리 활성화 (빠른 처리, 메모리 사용량 증가)'
    )
    
    # 워크플로우 선택 (상호 배타적)
    workflow_group = parser.add_mutually_exclusive_group()
    
    workflow_group.add_argument(
        '--full-auto', 
        action='store_true', 
        help='전체 자동화 워크플로우 (기본 + Unity 배치 모드)'
    )
    
    workflow_group.add_argument(
        '--build-webgl', 
        action='store_true', 
        help='WebGL 빌드 자동화 워크플로우'
    )
    
    workflow_group.add_argument(
        '--maintenance', 
        action='store_true', 
        help='유지보수 워크플로우 (검증, 호환성 검사, Git 상태)'
    )
    
    # 개별 기능들 (상호 배타적)
    individual_group = parser.add_mutually_exclusive_group()
    
    individual_group.add_argument(
        '--utf8-only', 
        action='store_true', 
        help='UTF-8 변환만 실행'
    )
    
    individual_group.add_argument(
        '--unity6-only', 
        action='store_true', 
        help='Unity 6 API 호환성 수정만 실행'
    )
    
    individual_group.add_argument(
        '--packages-only', 
        action='store_true', 
        help='Unity 패키지 업데이트만 실행'
    )
    
    individual_group.add_argument(
        '--git-only', 
        action='store_true', 
        help='Git 커밋 및 푸시만 실행'
    )
    
    individual_group.add_argument(
        '--unity-batch-only', 
        action='store_true', 
        help='Unity 배치 모드만 실행'
    )
    
    # 빌드 관련 옵션들
    build_group = parser.add_argument_group('빌드 옵션')
    
    build_group.add_argument(
        '--clean-builds', 
        action='store_true', 
        help='빌드 출력물 정리'
    )
    
    build_group.add_argument(
        '--build-target', 
        default='WebGL', 
        choices=['WebGL', 'Windows', 'Android', 'iOS'],
        help='빌드 타겟 선택 (기본값: WebGL)'
    )
    
    # Git 관련 옵션들
    git_group = parser.add_argument_group('Git 옵션')
    
    git_group.add_argument(
        '--commit-message', 
        default='Auto commit: Unity project updates',
        help='Git 커밋 메시지 (기본값: "Auto commit: Unity project updates")'
    )
    
    git_group.add_argument(
        '--skip-git', 
        action='store_true', 
        help='Git 작업 건너뛰기'
    )
    
    # 기타 옵션들
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true', 
        help='상세한 로그 출력'
    )
    
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='실제 실행 없이 계획만 출력'
    )
    
    return parser


def print_execution_plan(args, toolkit: UnityToolkit):
    """실행 계획을 출력합니다."""
    print("=== 실행 계획 ===")
    print(f"대상 프로젝트: {len(toolkit.get_projects())}개")
    
    for i, project_path in enumerate(toolkit.get_projects(), 1):
        project_name = project_path.split('\\')[-1] if '\\' in project_path else project_path.split('/')[-1]
        print(f"  {i}. {project_name}")
    
    print(f"\n실행할 작업:")
    
    if args.full_auto:
        print("  ✅ 전체 자동화 워크플로우")
        print("    - UTF-8 인코딩 변환")
        print("    - Unity 6 API 호환성 수정")
        print("    - Unity 패키지 업데이트")
        print("    - Git 커밋 및 푸시")
        print("    - Unity 배치 모드 실행")
    elif args.build_webgl:
        print("  ✅ WebGL 빌드 자동화 워크플로우")
        print(f"    - 빌드 타겟: {args.build_target}")
        print(f"    - 병렬 빌드: {'활성화' if args.parallel else '비활성화'}")
    elif args.maintenance:
        print("  ✅ 유지보수 워크플로우")
        print("    - 프로젝트 상태 검증")
        print("    - Unity 6 호환성 검사")
        print("    - Git 상태 확인")
    elif args.utf8_only:
        print("  ✅ UTF-8 인코딩 변환만")
    elif args.unity6_only:
        print("  ✅ Unity 6 API 호환성 수정만")
    elif args.packages_only:
        print("  ✅ Unity 패키지 업데이트만")
    elif args.git_only:
        print("  ✅ Git 커밋 및 푸시만")
    elif args.unity_batch_only:
        print("  ✅ Unity 배치 모드만")
    else:
        print("  ✅ 기본 자동화 워크플로우")
        print("    - UTF-8 인코딩 변환")
        print("    - Unity 6 API 호환성 수정")
        print("    - Unity 패키지 업데이트")
        if not args.skip_git:
            print("    - Git 커밋 및 푸시")
    
    print(f"\n추가 옵션:")
    print(f"  병렬 처리: {'활성화' if args.parallel else '비활성화'}")
    print(f"  Git 작업: {'건너뛰기' if args.skip_git else '포함'}")
    print(f"  커밋 메시지: {args.commit_message}")
    print(f"  상세 로그: {'활성화' if args.verbose else '비활성화'}")
    
    print("=" * 50)


def execute_workflow(args, toolkit: UnityToolkit) -> bool:
    """선택된 워크플로우를 실행합니다."""
    try:
        if args.full_auto:
            # 전체 자동화 워크플로우
            results = toolkit.full_automation_workflow(
                commit_message=args.commit_message,
                include_unity_batch=True,
                parallel_processing=args.parallel
            )
            return all(
                all(step_results.values()) if isinstance(step_results, dict) else step_results
                for step_results in results.values() if step_results is not None
            )
        
        elif args.build_webgl:
            # WebGL 빌드 워크플로우
            results = toolkit.build_automation_workflow(
                build_target=args.build_target,
                parallel_build=args.parallel,
                clean_before_build=args.clean_builds
            )
            return any(result for _, result in results)
        
        elif args.maintenance:
            # 유지보수 워크플로우
            results = toolkit.maintenance_workflow()
            return True  # 유지보수는 항상 성공으로 처리
        
        elif args.utf8_only:
            # UTF-8 변환만
            results = toolkit.convert_all_to_utf8()
            return any(results.values())
        
        elif args.unity6_only:
            # Unity 6 API 수정만
            results = toolkit.fix_all_unity6_apis()
            return any(results.values())
        
        elif args.packages_only:
            # 패키지 업데이트만
            results = toolkit.update_all_packages()
            return any(results.values())
        
        elif args.git_only:
            # Git 작업만
            results = toolkit.commit_all_changes(args.commit_message)
            return any(results.values())
        
        elif args.unity_batch_only:
            # Unity 배치 모드만
            if args.parallel:
                results = toolkit.run_unity_batch_parallel()
            else:
                results = toolkit.run_unity_batch_sequential()
            return any(results.values())
        
        else:
            # 기본 자동화 워크플로우
            results = toolkit.full_automation_workflow(
                commit_message=args.commit_message,
                include_unity_batch=False,
                parallel_processing=args.parallel
            )
            return all(
                all(step_results.values()) if isinstance(step_results, dict) else step_results
                for step_results in results.values() if step_results is not None
            )
    
    except Exception as e:
        print(f"❌ 워크플로우 실행 중 오류 발생: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def main_cli():
    """메인 CLI 진입점"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # 프로젝트 경로 설정
    project_paths = args.projects if args.projects else DEFAULT_PROJECT_PATHS
    
    if not project_paths:
        print("❌ 처리할 Unity 프로젝트가 지정되지 않았습니다.")
        print("   --projects 옵션을 사용하거나 설정 파일에서 DEFAULT_PROJECT_PATHS를 설정하세요.")
        return 1
    
    # UnityToolkit 초기화
    toolkit = UnityToolkit(project_paths)
    
    # 프로젝트 요약 출력
    if args.verbose:
        toolkit.print_project_summary()
    
    # 실행 계획 출력
    if args.dry_run or args.verbose:
        print_execution_plan(args, toolkit)
    
    # Dry run인 경우 여기서 종료
    if args.dry_run:
        print("🔍 Dry run 모드: 실제 실행하지 않고 계획만 출력했습니다.")
        return 0
    
    # 빌드 정리만 실행하는 경우
    if args.clean_builds and not (args.build_webgl or args.full_auto):
        print("🧹 빌드 출력물 정리 중...")
        toolkit.build_manager.clean_build_outputs(toolkit.get_projects())
        print("✅ 빌드 출력물 정리 완료")
        return 0
    
    # 워크플로우 실행
    print("🚀 워크플로우 실행 시작...\n")
    success = execute_workflow(args, toolkit)
    
    # 결과 출력
    if success:
        print("\n✅ 모든 작업이 성공적으로 완료되었습니다!")
        return 0
    else:
        print("\n❌ 일부 작업이 실패했습니다. 로그를 확인해주세요.")
        return 1


if __name__ == "__main__":
    sys.exit(main_cli()) 