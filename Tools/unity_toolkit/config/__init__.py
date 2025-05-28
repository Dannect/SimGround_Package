"""
Unity 툴킷 설정 모듈

모든 설정값들을 중앙에서 관리합니다.
"""

from .settings import *

__all__ = [
    'DEFAULT_PROJECT_PATHS',
    'DEFAULT_GIT_PACKAGES', 
    'UNITY_EDITOR_PATH',
    'UTF8_TARGET_EXTENSIONS',
    'EXCLUDED_DIRECTORIES'
] 