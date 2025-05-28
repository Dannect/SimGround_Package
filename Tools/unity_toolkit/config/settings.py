"""
Unity 툴킷 설정 파일

모든 설정값들을 중앙에서 관리하는 설정 모듈입니다.
기존 스크립트의 하드코딩된 값들을 여기서 관리합니다.
"""

import os
from typing import List, Dict

# =========================
# #region 프로젝트 설정
# =========================

# Unity 프로젝트 경로들 (기존 project_dirs)
DEFAULT_PROJECT_PATHS: List[str] = [
    r"E:\5.1.3.3_Experiment",
    r"E:\TDS",
    # 추가 프로젝트 경로들을 여기에 추가하세요
    # 예시:
    # r"E:\Project1",
    # r"E:\Project2",
    # r"E:\Project3",
]

# Unity 프로젝트 자동 스캔 기본 디렉토리
AUTO_SCAN_BASE_DIRECTORIES: List[str] = [
    # r"E:\UnityProjects",  # 주석 해제하여 자동 스캔 활성화
]

# =========================
# #region Git 설정
# =========================

# Git 패키지 설정 (기존 git_packages)
DEFAULT_GIT_PACKAGES: Dict[str, str] = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    # 필요시 추가 패키지들을 여기에 추가하세요
}

# Git 저장소 설정
GIT_BASE_URL: str = "https://github.com/Dannect/"
DEFAULT_BRANCH: str = "main"
DEV_BRANCH: str = "dev"

# Git 커밋 메시지 템플릿
DEFAULT_COMMIT_MESSAGE: str = "Auto commit: Unity project updates"

# =========================
# #region Unity Editor 설정
# =========================

# Unity Editor 경로 (기존 UNITY_EDITOR_PATH)
UNITY_EDITOR_PATH: str = r"D:\Unity\6000.0.30f1\Editor\Unity.exe"

# Unity 실행 타임아웃 설정
UNITY_TIMEOUT: int = 300  # 5분
UNITY_LOG_LEVEL: str = "info"  # debug, info, warning, error

# Unity 자동 경로 검색 디렉토리들
UNITY_SEARCH_PATHS: List[str] = [
    r"C:\Program Files\Unity\Hub\Editor",
    r"C:\Program Files\Unity\Editor", 
    r"C:\Program Files (x86)\Unity\Hub\Editor",
    r"C:\Program Files (x86)\Unity\Editor",
    r"D:\Unity",  # 사용자 정의 경로
]

# =========================
# #region 빌드 설정
# =========================

# WebGL 빌드 설정
BUILD_TARGET: str = "WebGL"
DEFAULT_BUILD_TARGET: str = "webgl"
BUILD_OUTPUT_DIR: str = "Builds"  # 프로젝트 내 빌드 출력 폴더
BUILD_TIMEOUT: int = 1800  # WebGL 빌드 타임아웃 (30분)

# WebGL Player Settings 기본값
WEBGL_DEFAULT_SETTINGS = {
    "productName": "Science Experiment Simulation",
    "companyName": "Educational Software", 
    "bundleVersion": "1.0.0",
    "defaultWebScreenWidth": 1655,
    "defaultWebScreenHeight": 892,
    "template": "APPLICATION:Minimal",
    "compressionFormat": "Disabled",  # WebGLCompressionFormat.Disabled
    "memorySize": 32,  # Initial Memory Size (MB)
    "maximumMemorySize": 2048,  # Maximum Memory Size (MB)
}

# =========================
# #region 병렬 처리 설정
# =========================

# 병렬 처리 기본 설정
DEFAULT_MAX_WORKERS: int = 3  # Unity 배치 모드 병렬 처리
BUILD_MAX_WORKERS: int = 2    # WebGL 빌드 병렬 처리

# =========================
# #region 파일 처리 설정
# =========================

# UTF-8 변환 대상 파일 확장자
UTF8_TARGET_EXTENSIONS: List[str] = [".cs"]

# Unity 6 API 호환성 수정 대상 파일 확장자
API_FIX_TARGET_EXTENSIONS: List[str] = [".cs"]

# 제외할 디렉토리들
EXCLUDED_DIRECTORIES: List[str] = [
    "Library", 
    "Temp", 
    "Logs", 
    "obj", 
    "bin",
    ".git",
    ".vs",
    ".vscode"
]

# =========================
# #region Unity 6 API 호환성 설정
# =========================

# Unity 6에서 deprecated된 API 교체 규칙들
UNITY6_API_REPLACEMENTS = [
    # FindObjectOfType -> FindFirstObjectByType
    (r'FindObjectOfType<([^>]+)>\(\)', r'FindFirstObjectByType<\1>()'),
    (r'GameObject\.FindObjectOfType<([^>]+)>\(\)', r'FindFirstObjectByType<\1>()'),
    (r'Object\.FindObjectOfType<([^>]+)>\(\)', r'FindFirstObjectByType<\1>()'),
    
    # FindObjectsOfType -> FindObjectsByType
    (r'FindObjectsOfType<([^>]+)>\(\)', r'FindObjectsByType<\1>(FindObjectsSortMode.None)'),
    (r'GameObject\.FindObjectsOfType<([^>]+)>\(\)', r'FindObjectsByType<\1>(FindObjectsSortMode.None)'),
    (r'Object\.FindObjectsOfType<([^>]+)>\(\)', r'FindObjectsByType<\1>(FindObjectsSortMode.None)'),
    
    # Unity 6 WebGL API 호환성 수정
    (r'PlayerSettings\.WebGL\.debugSymbols\s*=\s*false', r'PlayerSettings.WebGL.debugSymbolMode = WebGLDebugSymbolMode.Off'),
    (r'PlayerSettings\.WebGL\.debugSymbols\s*=\s*true', r'PlayerSettings.WebGL.debugSymbolMode = WebGLDebugSymbolMode.External'),
    (r'PlayerSettings\.WebGL\.wasmStreaming\s*=\s*[^;]+;', r'// Unity 6에서 wasmStreaming 제거됨 (decompressionFallback에 따라 자동 결정)'),
    (r'PlayerSettings\.SplashScreen\.logoAnimationMode[^;]+;', r'// Unity 6에서 logoAnimationMode 제거됨'),
    (r'PlayerSettings\.GetIconsForTargetGroup\(BuildTargetGroup\.([^)]+)\)', 
     r'PlayerSettings.GetIcons(NamedBuildTarget.\1, IconKind.Application)'),
]

# =========================
# #region 로깅 설정
# =========================

# 로그 레벨 설정
LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR

# 로그 파일 설정
LOG_TO_FILE: bool = True
LOG_FILE_PATH: str = "unity_toolkit.log"
LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT: int = 5

# =========================
# #region 환경별 설정 오버라이드
# =========================

def get_environment_config():
    """환경별 설정을 반환합니다."""
    env = os.environ.get('UNITY_TOOLKIT_ENV', 'development')
    
    if env == 'production':
        return {
            'LOG_LEVEL': 'WARNING',
            'UNITY_TIMEOUT': 600,  # 10분
            'BUILD_TIMEOUT': 3600,  # 60분
            'DEFAULT_MAX_WORKERS': 2,
            'BUILD_MAX_WORKERS': 1,
        }
    elif env == 'testing':
        return {
            'LOG_LEVEL': 'DEBUG',
            'UNITY_TIMEOUT': 60,   # 1분
            'BUILD_TIMEOUT': 300,  # 5분
            'DEFAULT_MAX_WORKERS': 1,
            'BUILD_MAX_WORKERS': 1,
        }
    else:  # development
        return {
            'LOG_LEVEL': 'INFO',
            'UNITY_TIMEOUT': 300,  # 5분
            'BUILD_TIMEOUT': 1800, # 30분
            'DEFAULT_MAX_WORKERS': 3,
            'BUILD_MAX_WORKERS': 2,
        }

# 환경별 설정 적용
_env_config = get_environment_config()
LOG_LEVEL = _env_config.get('LOG_LEVEL', LOG_LEVEL)
UNITY_TIMEOUT = _env_config.get('UNITY_TIMEOUT', UNITY_TIMEOUT)
BUILD_TIMEOUT = _env_config.get('BUILD_TIMEOUT', BUILD_TIMEOUT)
DEFAULT_MAX_WORKERS = _env_config.get('DEFAULT_MAX_WORKERS', DEFAULT_MAX_WORKERS)
BUILD_MAX_WORKERS = _env_config.get('BUILD_MAX_WORKERS', BUILD_MAX_WORKERS)

# =========================
# #region 설정 검증 함수들
# =========================

def validate_unity_editor_path() -> bool:
    """Unity Editor 경로가 유효한지 확인합니다."""
    return os.path.exists(UNITY_EDITOR_PATH)

def validate_project_paths(project_paths: List[str] = None) -> List[str]:
    """유효한 Unity 프로젝트 경로들만 반환합니다."""
    paths_to_check = project_paths if project_paths is not None else DEFAULT_PROJECT_PATHS
    valid_paths = []
    for path in paths_to_check:
        if os.path.exists(path):
            project_settings = os.path.join(path, "ProjectSettings", "ProjectSettings.asset")
            if os.path.exists(project_settings):
                valid_paths.append(path)
    return valid_paths

def get_auto_discovered_projects() -> List[str]:
    """자동 스캔으로 발견된 Unity 프로젝트들을 반환합니다."""
    discovered_projects = []
    
    for base_dir in AUTO_SCAN_BASE_DIRECTORIES:
        if not os.path.exists(base_dir):
            continue
            
        try:
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path):
                    # Unity 프로젝트인지 확인
                    project_settings = os.path.join(item_path, "ProjectSettings")
                    assets_folder = os.path.join(item_path, "Assets")
                    
                    if os.path.exists(project_settings) and os.path.exists(assets_folder):
                        discovered_projects.append(item_path)
        except Exception:
            continue
    
    return discovered_projects

def get_all_project_paths() -> List[str]:
    """설정된 프로젝트 경로와 자동 발견된 프로젝트 경로를 모두 반환합니다."""
    all_paths = DEFAULT_PROJECT_PATHS.copy()
    all_paths.extend(get_auto_discovered_projects())
    
    # 중복 제거 및 유효성 검증
    unique_paths = list(set(all_paths))
    return validate_project_paths() if unique_paths else []

# =========================
# #region 설정 정보 출력
# =========================

def print_current_settings():
    """현재 설정 정보를 출력합니다."""
    print("=== Unity 툴킷 현재 설정 ===")
    print(f"Unity Editor 경로: {UNITY_EDITOR_PATH}")
    print(f"Unity Editor 유효성: {'✅ 유효' if validate_unity_editor_path() else '❌ 무효'}")
    print(f"기본 프로젝트 수: {len(DEFAULT_PROJECT_PATHS)}")
    print(f"유효한 프로젝트 수: {len(validate_project_paths())}")
    print(f"Git 패키지 수: {len(DEFAULT_GIT_PACKAGES)}")
    print(f"빌드 타겟: {BUILD_TARGET}")
    print(f"병렬 처리 워커 수: {DEFAULT_MAX_WORKERS}")
    print(f"빌드 병렬 워커 수: {BUILD_MAX_WORKERS}")
    print(f"로그 레벨: {LOG_LEVEL}")
    print(f"환경: {os.environ.get('UNITY_TOOLKIT_ENV', 'development')}")
    print("=" * 40) 