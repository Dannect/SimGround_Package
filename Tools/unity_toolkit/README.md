# Unity 툴킷 (Unity Toolkit)

Unity 프로젝트 개발을 자동화하기 위한 종합 도구 모음입니다. 기존의 1600줄 단일 스크립트를 모듈화하여 유지보수성과 재사용성을 크게 개선했습니다.

## 🚀 주요 기능

- **UTF-8 인코딩 변환**: C# 스크립트 파일을 UTF-8로 일괄 변환
- **Unity 6 API 호환성**: Deprecated API를 최신 API로 자동 교체
- **Git 저장소 관리**: 자동 커밋, 푸시, 브랜치 관리
- **Unity 패키지 관리**: Git 패키지 자동 추가 및 업데이트
- **WebGL 빌드 자동화**: Player Settings 완전 반영 빌드
- **Unity CLI 배치 처리**: Editor 스크립트 자동 실행
- **프로젝트 유지보수**: 상태 검증, 호환성 검사

## 📁 프로젝트 구조

```
unity_toolkit/
├── __init__.py                 # 패키지 초기화
├── unity_toolkit.py           # 통합 인터페이스 클래스
├── config/
│   └── settings.py            # 모든 설정 중앙 관리
├── core/
│   └── project_manager.py     # 프로젝트 관리
├── encoding/
│   └── utf8_converter.py      # UTF-8 변환
├── git/
│   └── repository_manager.py  # Git 저장소 관리
├── unity/
│   ├── package_manager.py     # Unity 패키지 관리
│   ├── build_manager.py       # Unity 빌드 관리
│   └── api_compatibility.py   # Unity 6 API 호환성
└── cli/
    └── main_cli.py            # 명령줄 인터페이스
```

## ⚙️ 설치 및 설정

### 1. 기본 설정

`config/settings.py` 파일에서 프로젝트 경로와 Unity Editor 경로를 설정하세요:

```python
# Unity 프로젝트 경로들
DEFAULT_PROJECT_PATHS: List[str] = [
    r"E:\5.1.3.3_Experiment",
    r"E:\TDS",
    r"E:\YourProject1",
    r"E:\YourProject2",
]

# Unity Editor 경로
UNITY_EDITOR_PATH: str = r"D:\Unity\6000.0.30f1\Editor\Unity.exe"
```

### 2. Git 패키지 설정

필요한 Git 패키지들을 설정하세요:

```python
DEFAULT_GIT_PACKAGES: Dict[str, str] = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
}
```

## 🎯 사용 방법

### 1. 명령줄 인터페이스 (CLI) 사용

#### 기본 자동화 워크플로우
```bash
# 기본 워크플로우 (UTF-8 변환 → Unity 6 API 수정 → 패키지 업데이트 → Git 커밋)
python -m unity_toolkit

# 상세 로그와 함께 실행
python -m unity_toolkit --verbose

# 실행 계획만 확인 (실제 실행 안함)
python -m unity_toolkit --dry-run
```

#### 전체 자동화 워크플로우
```bash
# 기본 워크플로우 + Unity 배치 모드 실행
python -m unity_toolkit --full-auto

# 병렬 처리로 빠르게 실행
python -m unity_toolkit --full-auto --parallel
```

#### WebGL 빌드 자동화
```bash
# WebGL 빌드 자동화 (Player Settings 완전 반영)
python -m unity_toolkit --build-webgl

# 병렬 빌드로 빠르게 실행
python -m unity_toolkit --build-webgl --parallel

# 빌드 전 출력물 정리
python -m unity_toolkit --build-webgl --clean-builds
```

#### 개별 기능 실행
```bash
# UTF-8 변환만 실행
python -m unity_toolkit --utf8-only

# Unity 6 API 호환성 수정만 실행
python -m unity_toolkit --unity6-only

# Unity 패키지 업데이트만 실행
python -m unity_toolkit --packages-only

# Git 커밋 및 푸시만 실행
python -m unity_toolkit --git-only

# Unity 배치 모드만 실행
python -m unity_toolkit --unity-batch-only
```

#### 유지보수 워크플로우
```bash
# 프로젝트 검증, 호환성 검사, Git 상태 확인
python -m unity_toolkit --maintenance
```

#### 특정 프로젝트만 처리
```bash
# 특정 프로젝트 경로 지정
python -m unity_toolkit --projects "C:\Project1" "C:\Project2"

# Git 작업 건너뛰기
python -m unity_toolkit --skip-git

# 커스텀 커밋 메시지
python -m unity_toolkit --commit-message "Custom commit message"
```

### 2. Python 코드에서 사용

#### 통합 인터페이스 사용
```python
from unity_toolkit import UnityToolkit

# 툴킷 초기화
toolkit = UnityToolkit([
    r"E:\Project1",
    r"E:\Project2"
])

# 전체 자동화 워크플로우 실행
results = toolkit.full_automation_workflow(
    commit_message="Auto update: Unity projects",
    include_unity_batch=True,
    parallel_processing=True
)

# WebGL 빌드 자동화
build_results = toolkit.build_automation_workflow(
    build_target="WebGL",
    parallel_build=True,
    clean_before_build=True
)

# 유지보수 워크플로우
maintenance_results = toolkit.maintenance_workflow()
```

#### 개별 모듈 사용
```python
from unity_toolkit import UTF8Converter, GitRepositoryManager, UnityBuildManager

# UTF-8 변환만 필요한 경우
converter = UTF8Converter()
converter.convert_project_files(r"E:\Project1")

# Git 관리만 필요한 경우
git_manager = GitRepositoryManager()
git_manager.commit_and_push_changes(r"E:\Project1", "Update project")

# Unity 빌드만 필요한 경우
build_manager = UnityBuildManager()
build_manager.run_unity_webgl_build(r"E:\Project1")
```

## 🔧 고급 설정

### 환경별 설정

환경 변수를 통해 다른 설정을 적용할 수 있습니다:

```bash
# 개발 환경 (기본값)
set UNITY_TOOLKIT_ENV=development

# 프로덕션 환경 (더 보수적인 설정)
set UNITY_TOOLKIT_ENV=production

# 테스트 환경 (빠른 타임아웃)
set UNITY_TOOLKIT_ENV=testing
```

### 병렬 처리 설정

`config/settings.py`에서 병렬 처리 워커 수를 조정할 수 있습니다:

```python
# Unity 배치 모드 병렬 처리
DEFAULT_MAX_WORKERS: int = 3

# WebGL 빌드 병렬 처리
BUILD_MAX_WORKERS: int = 2
```

### Unity 6 API 호환성 규칙 추가

새로운 API 교체 규칙을 추가할 수 있습니다:

```python
UNITY6_API_REPLACEMENTS = [
    # 기존 규칙들...
    
    # 새로운 규칙 추가
    (r'OldAPI\.Method\(\)', r'NewAPI.Method()'),
]
```

## 📊 워크플로우 상세 설명

### 기본 자동화 워크플로우
1. **UTF-8 인코딩 변환**: 모든 C# 파일을 UTF-8로 변환
2. **Unity 6 API 호환성 수정**: Deprecated API를 최신 API로 교체
3. **Unity 패키지 업데이트**: Git 패키지들을 manifest.json에 추가
4. **Git 커밋 및 푸시**: 변경사항을 자동으로 커밋하고 푸시

### 전체 자동화 워크플로우
- 기본 워크플로우 + Unity 배치 모드 실행
- Editor 스크립트들이 자동으로 실행됨

### WebGL 빌드 자동화 워크플로우
1. **빌드 출력물 정리** (선택사항)
2. **Player Settings 자동 설정**: 과학실험 시뮬레이션에 최적화된 설정 적용
3. **WebGL 빌드 실행**: Unity CLI를 통한 자동 빌드
4. **빌드 결과 검증**: 성공/실패 여부 확인

### 유지보수 워크플로우
1. **프로젝트 상태 검증**: Unity 프로젝트 유효성 확인
2. **Unity 6 호환성 검사**: Deprecated API 사용 여부 검사
3. **Git 상태 확인**: 저장소 상태 및 브랜치 정보 확인

## 🎮 Unity 6 호환성 수정

자동으로 수정되는 API들:

| 기존 API | 새로운 API |
|----------|------------|
| `FindObjectOfType<T>()` | `FindFirstObjectByType<T>()` |
| `FindObjectsOfType<T>()` | `FindObjectsByType<T>(FindObjectsSortMode.None)` |
| `PlayerSettings.WebGL.debugSymbols` | `PlayerSettings.WebGL.debugSymbolMode` |
| `PlayerSettings.GetIconsForTargetGroup()` | `PlayerSettings.GetIcons()` |

## 🌐 WebGL 빌드 최적화

과학실험 시뮬레이션에 최적화된 WebGL 설정:

- **해상도**: 1655x892 (교육용 최적화)
- **템플릿**: Minimal (빠른 로딩)
- **메모리**: 초기 32MB, 최대 2048MB
- **압축**: 비활성화 (호환성 우선)
- **예외 지원**: 명시적 예외만 (성능 최적화)

## 🔍 문제 해결

### 일반적인 문제들

#### Unity Editor 경로 오류
```bash
❌ Unity 경로를 찾을 수 없습니다: D:\Unity\6000.0.30f1\Editor\Unity.exe
```
**해결책**: `config/settings.py`에서 `UNITY_EDITOR_PATH`를 올바른 경로로 수정

#### 프로젝트 경로 오류
```bash
❌ 처리할 Unity 프로젝트가 지정되지 않았습니다.
```
**해결책**: `--projects` 옵션 사용하거나 `DEFAULT_PROJECT_PATHS` 설정

#### Git 저장소 오류
```bash
❌ Git 리포지토리 초기화 실패
```
**해결책**: 프로젝트 폴더에서 `git init` 수동 실행 후 재시도

### 로그 확인

상세한 로그를 확인하려면:
```bash
python -m unity_toolkit --verbose
```

## 📈 성능 최적화

### 병렬 처리 활용
- Unity 배치 모드: 최대 3개 프로젝트 동시 처리
- WebGL 빌드: 최대 2개 프로젝트 동시 빌드

### 메모리 사용량 최적화
- 대용량 프로젝트는 순차 처리 권장
- 병렬 처리 시 시스템 메모리 8GB 이상 권장

## 🤝 기여하기

1. 새로운 기능은 별도 모듈로 분리
2. 설정값은 `config/settings.py`에 추가
3. CLI 옵션은 `cli/main_cli.py`에 추가
4. 각 모듈은 단일 책임 원칙 준수

## 📝 라이선스

이 프로젝트는 교육용 목적으로 개발되었습니다.

## 🔗 관련 링크

- [Unity 6 API 변경사항](https://docs.unity3d.com/6000.0/Documentation/Manual/UpgradeGuides.html)
- [WebGL 최적화 가이드](https://docs.unity3d.com/Manual/webgl-building.html)
- [Git 패키지 관리](https://docs.unity3d.com/Manual/upm-git.html)

---

**개발자**: Dannect  
**버전**: 1.0.0  
**최종 업데이트**: 2024년 