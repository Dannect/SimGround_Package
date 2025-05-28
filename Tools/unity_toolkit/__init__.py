"""
Unity 개발 자동화 툴킷

이 패키지는 Unity 프로젝트 개발을 자동화하기 위한 다양한 도구들을 제공합니다.

주요 기능:
- UTF-8 인코딩 변환
- Unity 6 API 호환성 수정
- Git 저장소 관리
- Unity 패키지 관리
- WebGL 빌드 자동화
- Unity CLI 배치 처리
"""

__version__ = "1.0.0"
__author__ = "Dannect"

# 주요 모듈들을 임포트하여 쉽게 접근할 수 있도록 함
from .core.project_manager import ProjectManager
from .encoding.utf8_converter import UTF8Converter
from .git.repository_manager import GitRepositoryManager
from .unity.package_manager import UnityPackageManager
from .unity.build_manager import UnityBuildManager
from .unity.api_compatibility import Unity6APIFixer
from .cli.main_cli import main_cli

# 편의를 위한 통합 클래스
from .unity_toolkit import UnityToolkit

__all__ = [
    'UnityToolkit',
    'ProjectManager',
    'UTF8Converter', 
    'GitRepositoryManager',
    'UnityPackageManager',
    'UnityBuildManager',
    'Unity6APIFixer',
    'main_cli'
] 