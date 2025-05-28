# Unity 툴킷 빠른 시작 가이드

Unity 프로젝트 자동화를 5분 안에 시작해보세요!

## 🚀 1단계: 설정

### 프로젝트 경로 설정
`config/settings.py` 파일을 열고 Unity 프로젝트 경로들을 추가하세요:

```python
DEFAULT_PROJECT_PATHS: List[str] = [
    r"E:\YourProject1",
    r"E:\YourProject2",
    # 여기에 더 많은 프로젝트 경로 추가
]
```

### Unity Editor 경로 설정
Unity Editor 설치 경로를 확인하고 설정하세요:

```python
UNITY_EDITOR_PATH: str = r"D:\Unity\6000.0.30f1\Editor\Unity.exe"
```

## ⚡ 2단계: 기본 사용법

### 가장 간단한 사용법
```bash
# 모든 프로젝트에 기본 자동화 적용
python -m unity_toolkit
```

이 명령어 하나로 다음 작업이 자동 실행됩니다:
- ✅ UTF-8 인코딩 변환
- ✅ Unity 6 API 호환성 수정  
- ✅ Unity 패키지 업데이트
- ✅ Git 커밋 및 푸시

### 실행 전 미리보기
```bash
# 실제 실행하지 않고 계획만 확인
python -m unity_toolkit --dry-run
```

### 상세 로그 확인
```bash
# 자세한 실행 과정 확인
python -m unity_toolkit --verbose
```

## 🎯 3단계: 주요 기능들

### WebGL 빌드 자동화
```bash
# WebGL 빌드 (Player Settings 자동 설정 포함)
python -m unity_toolkit --build-webgl
```

### 전체 자동화 (Unity 배치 모드 포함)
```bash
# 기본 자동화 + Unity Editor 스크립트 실행
python -m unity_toolkit --full-auto
```

### 병렬 처리로 빠르게
```bash
# 여러 프로젝트를 동시에 처리
python -m unity_toolkit --full-auto --parallel
```

### 특정 프로젝트만 처리
```bash
# 원하는 프로젝트만 선택
python -m unity_toolkit --projects "C:\Project1" "C:\Project2"
```

## 🔧 4단계: 개별 기능 사용

필요한 기능만 선택적으로 실행할 수 있습니다:

```bash
# UTF-8 변환만
python -m unity_toolkit --utf8-only

# Unity 6 API 수정만  
python -m unity_toolkit --unity6-only

# 패키지 업데이트만
python -m unity_toolkit --packages-only

# Git 커밋만
python -m unity_toolkit --git-only

# Unity 배치 모드만
python -m unity_toolkit --unity-batch-only
```

## 🛠️ 5단계: 문제 해결

### 자주 발생하는 문제들

#### "Unity 경로를 찾을 수 없습니다"
```bash
❌ Unity 경로를 찾을 수 없습니다: D:\Unity\6000.0.30f1\Editor\Unity.exe
```
**해결**: `config/settings.py`에서 `UNITY_EDITOR_PATH`를 실제 Unity 설치 경로로 수정

#### "처리할 Unity 프로젝트가 지정되지 않았습니다"
```bash
❌ 처리할 Unity 프로젝트가 지정되지 않았습니다.
```
**해결**: `config/settings.py`에서 `DEFAULT_PROJECT_PATHS`에 프로젝트 경로 추가

#### Git 관련 오류
```bash
❌ Git 리포지토리 초기화 실패
```
**해결**: 프로젝트 폴더에서 수동으로 `git init` 실행

### 로그 확인하기
문제가 발생하면 상세 로그를 확인하세요:
```bash
python -m unity_toolkit --verbose
```

## 📚 더 자세한 정보

- 📖 [전체 사용법 가이드](README.md)
- 🔧 [고급 설정 방법](README.md#고급-설정)
- 🎮 [Unity 6 호환성](README.md#unity-6-호환성-수정)
- 🌐 [WebGL 빌드 최적화](README.md#webgl-빌드-최적화)

## 💡 팁

1. **첫 실행 시**: `--dry-run`으로 계획 확인 후 실행
2. **대용량 프로젝트**: `--parallel` 없이 순차 처리 권장
3. **정기 유지보수**: `--maintenance`로 프로젝트 상태 점검
4. **빠른 빌드**: `--build-webgl --parallel`로 병렬 빌드

---

🎉 **축하합니다!** Unity 프로젝트 자동화를 시작했습니다.  
더 궁금한 점이 있으면 [README.md](README.md)를 참고하세요. 