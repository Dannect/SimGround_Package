#!/usr/bin/env python3
"""
Unity 툴킷 테스트 스크립트
"""

def test_imports():
    """모든 모듈 임포트 테스트"""
    print("=== Unity 툴킷 임포트 테스트 ===")
    
    try:
        print("1. 설정 모듈 임포트...")
        from unity_toolkit.config.settings import DEFAULT_PROJECT_PATHS, DEFAULT_GIT_PACKAGES
        print(f"   ✅ 성공 - 프로젝트 수: {len(DEFAULT_PROJECT_PATHS)}")
        
        print("2. 핵심 모듈 임포트...")
        from unity_toolkit.core.project_manager import ProjectManager
        print("   ✅ 성공")
        
        print("3. 인코딩 모듈 임포트...")
        from unity_toolkit.encoding.utf8_converter import UTF8Converter
        print("   ✅ 성공")
        
        print("4. Git 모듈 임포트...")
        from unity_toolkit.git.repository_manager import GitRepositoryManager
        print("   ✅ 성공")
        
        print("5. Unity 모듈 임포트...")
        from unity_toolkit.unity.package_manager import UnityPackageManager
        from unity_toolkit.unity.build_manager import UnityBuildManager
        from unity_toolkit.unity.api_compatibility import Unity6APIFixer
        print("   ✅ 성공")
        
        print("6. CLI 모듈 임포트...")
        from unity_toolkit.cli.main_cli import main_cli
        print("   ✅ 성공")
        
        print("7. 통합 툴킷 임포트...")
        from unity_toolkit.unity_toolkit import UnityToolkit
        print("   ✅ 성공")
        
        print("\n🎉 모든 모듈 임포트 성공!")
        return True
        
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """기본 기능 테스트"""
    print("\n=== 기본 기능 테스트 ===")
    
    try:
        from unity_toolkit.config.settings import DEFAULT_PROJECT_PATHS
        from unity_toolkit.core.project_manager import ProjectManager
        
        print("1. ProjectManager 생성...")
        pm = ProjectManager(DEFAULT_PROJECT_PATHS)
        print("   ✅ 성공")
        
        print("2. 프로젝트 정보 출력...")
        pm.print_projects_summary()
        
        print("3. UTF8Converter 테스트...")
        from unity_toolkit.encoding.utf8_converter import UTF8Converter
        converter = UTF8Converter()
        print("   ✅ 성공")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli():
    """CLI 테스트"""
    print("\n=== CLI 테스트 ===")
    
    try:
        import sys
        from unity_toolkit.cli.main_cli import create_argument_parser
        
        print("1. 인수 파서 생성...")
        parser = create_argument_parser()
        print("   ✅ 성공")
        
        print("2. 도움말 테스트...")
        # 도움말 출력 (실제로는 출력하지 않음)
        help_text = parser.format_help()
        print(f"   ✅ 성공 - 도움말 길이: {len(help_text)} 문자")
        
        print("3. 기본 인수 파싱...")
        args = parser.parse_args(['--dry-run'])
        print(f"   ✅ 성공 - dry_run: {args.dry_run}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Unity 툴킷 테스트 시작...\n")
    
    success = True
    success &= test_imports()
    success &= test_basic_functionality()
    success &= test_cli()
    
    print(f"\n{'='*50}")
    if success:
        print("🎉 모든 테스트 통과!")
        exit(0)
    else:
        print("❌ 일부 테스트 실패")
        exit(1) 