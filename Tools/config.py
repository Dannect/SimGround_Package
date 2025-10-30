"""
Unity 프로젝트 자동화 도구 설정 및 상수 정의
"""
import os


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
    # Code Optimization (Unity 6.0의 WasmCodeOptimization)
    # 사용 가능한 옵션:
    #   - "BuildTimes": 빠른 빌드 시간 (개발용)
    #   - "RuntimeSpeed": 성능 최적화
    #   - "RuntimeSpeedLTO": 성능 최적화 + LTO (권장, 최고 성능)
    #   - "DiskSize": 크기 최적화
    #   - "DiskSizeLTO": 크기 최적화 + LTO (최소 크기)
    WEBGL_CODE_OPTIMIZATION = "RuntimeSpeed"
    
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


# 호환성을 위한 전역 변수들 (기존 코드와의 호환성 유지)
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

