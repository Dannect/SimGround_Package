# Unity 툴킷 사용법 가이드

## 🚀 빠른 시작

### 1. 기본 설정
`unity_toolkit/config/settings.py` 파일에서 프로젝트 경로를 설정하세요:

```python
DEFAULT_PROJECT_PATHS: List[str] = [
    r"E:\YourProject1",
    r"E:\YourProject2",
    # 여기에 Unity 프로젝트 경로들을 추가하세요
]
```

### 2. 기본 사용법

```bash
# 기본 자동화 워크플로우 (UTF-8 변환 + Unity 6 API 수정 + 패키지 업데이트 + Git 커밋)
py -m unity_toolkit

# 실행 전 미리보기 (실제 실행하지 않음)
py -m unity_toolkit --dry-run

# 상세한 로그와 함께 실행
py -m unity_toolkit --verbose
```

## 📋 주요 워크플로우

### 🔄 기본 자동화 워크플로우
```bash
py -m unity_toolkit
```
- ✅ UTF-8 인코딩 변환
- ✅ Unity 6 API 호환성 수정  
- ✅ Unity 패키지 업데이트
- ✅ Git 커밋 및 푸시

### 🚀 전체 자동화 워크플로우
```bash
py -m unity_toolkit --full-auto
```
기본 워크플로우 + Unity 배치 모드 실행

### 🌐 WebGL 빌드 자동화
```bash
py -m unity_toolkit --build-webgl
py -m unity_toolkit --build-webgl --parallel  # 병렬 빌드
```

### 🔧 유지보수 워크플로우
```bash
py -m unity_toolkit --maintenance
```
- 프로젝트 상태 검증
- Unity 6 호환성 검사
- Git 상태 확인

## 🎯 개별 기능 실행

### UTF-8 변환만
```bash
py -m unity_toolkit --utf8-only
```

### Unity 6 API 수정만
```bash
py -m unity_toolkit --unity6-only
```

### 패키지 업데이트만
```bash
py -m unity_toolkit --packages-only
```

### Git 작업만
```bash
py -m unity_toolkit --git-only
py -m unity_toolkit --git-only --commit-message "Custom commit message"
```

### Unity 배치 모드만
```bash
py -m unity_toolkit --unity-batch-only
py -m unity_toolkit --unity-batch-only --parallel  # 병렬 처리
```

## ⚙️ 고급 옵션

### 특정 프로젝트만 처리
```bash
py -m unity_toolkit --projects "C:\Project1" "C:\Project2"
```

### 병렬 처리 활성화
```bash
py -m unity_toolkit --parallel
```

### Git 작업 건너뛰기
```bash
py -m unity_toolkit --skip-git
```

### 빌드 출력물 정리
```bash
py -m unity_toolkit --clean-builds
```

### 다른 빌드 타겟
```bash
py -m unity_toolkit --build-webgl --build-target Windows
```

## 📊 실행 결과 예시

### 성공적인 실행
```
=== 실행 계획 ===
대상 프로젝트: 2개
  1. 5.1.3.3_Experiment
  2. TDS

실행할 작업:
  ✅ 기본 자동화 워크플로우
    - UTF-8 인코딩 변환
    - Unity 6 API 호환성 수정
    - Unity 패키지 업데이트
    - Git 커밋 및 푸시

🚀 워크플로우 실행 시작...

✅ 모든 작업이 성공적으로 완료되었습니다!
```

### Dry-run 모드
```
=== 실행 계획 ===
대상 프로젝트: 2개
  1. 5.1.3.3_Experiment
  2. TDS

🔍 Dry run 모드: 실제 실행하지 않고 계획만 출력했습니다.
```

## 🛠️ 문제 해결

### 모듈을 찾을 수 없는 경우
```bash
# 올바른 디렉토리에서 실행하세요
cd e:\SimGround_Package\Tools
py -m unity_toolkit
```

### Python 명령어가 작동하지 않는 경우
```bash
# python 대신 py 사용 (Windows)
py -m unity_toolkit

# 또는 전체 경로 사용
python.exe -m unity_toolkit
```

### 프로젝트가 인식되지 않는 경우
1. `config/settings.py`에서 `DEFAULT_PROJECT_PATHS` 확인
2. Unity 프로젝트 경로가 올바른지 확인
3. `--projects` 옵션으로 직접 지정

### 권한 오류가 발생하는 경우
```bash
# 관리자 권한으로 실행
# 또는 Git 저장소 권한 확인
```

## 📝 설정 파일 위치

- **메인 설정**: `unity_toolkit/config/settings.py`
- **프로젝트 경로**: `DEFAULT_PROJECT_PATHS`
- **Git 패키지**: `DEFAULT_GIT_PACKAGES`
- **Unity Editor 경로**: `UNITY_EDITOR_PATH`

## 🔍 로그 및 디버깅

### 상세 로그 확인
```bash
py -m unity_toolkit --verbose
```

### 실행 계획만 확인
```bash
py -m unity_toolkit --dry-run
```

### 테스트 실행
```bash
py test_toolkit.py
```

## 📚 추가 정보

- **README.md**: 전체 기능 설명
- **QUICK_START.md**: 빠른 시작 가이드
- **config/settings.py**: 모든 설정 옵션
- **test_toolkit.py**: 테스트 스크립트 