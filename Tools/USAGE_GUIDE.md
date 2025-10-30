# dannect.unity.toolkit.py 사용 가이드

Unity 6 프로젝트 자동화 도구 - 패키지 관리, Git 작업, 빌드 자동화

---

## 🚀 빠른 시작 (Quick Start)

### 기본 실행 방법

```powershell
# Tools 디렉토리로 이동
cd C:\Users\wkzkx\Desktop\Lim\GitHub\SimGround_Package\Tools

# 도움말 보기
python dannect.unity.toolkit.py --help

# 패키지 추가만 실행 (기본 모드)
python dannect.unity.toolkit.py

# WebGL 빌드 실행 (가장 많이 사용)
python dannect.unity.toolkit.py --build-webgl
```

---

## 📋 주요 명령어 모음 (복사해서 사용)

### 1. 패키지 관리

```powershell
# 패키지 추가만 실행 (Git 작업 없음)
python dannect.unity.toolkit.py --package-only

# 패키지 추가 + Git 커밋 (푸시 제외)
python dannect.unity.toolkit.py
python dannect.unity.toolkit.py --git-commit

# 패키지 추가 + Git 커밋 + 푸시
python dannect.unity.toolkit.py --git-push
```

### 2. WebGL 빌드

```powershell
# WebGL 순차 빌드 (안전, 느림)
python dannect.unity.toolkit.py --build-webgl

# WebGL 병렬 빌드 (빠름, 메모리 많이 사용)
python dannect.unity.toolkit.py --build-webgl --build-parallel

# WebGL 빌드만 (패키지 추가/Git 작업 스킵)
python dannect.unity.toolkit.py --build-only

# WebGL 빌드만 + 병렬 실행
python dannect.unity.toolkit.py --build-only --build-parallel
```

### 3. Unity 배치 모드

```powershell
# Unity 배치 모드 순차 실행
python dannect.unity.toolkit.py --unity-batch

# Unity 배치 모드 병렬 실행 (최대 3개 동시)
python dannect.unity.toolkit.py --unity-batch --parallel
```

### 4. 빌드 정리

```powershell
# 빌드 출력물 정리 (디스크 공간 확보)
python dannect.unity.toolkit.py --clean-builds
```

### 5. SystemManager 메소드 추가

```powershell
# SystemManager에 공통 메소드 추가 + Git 커밋
python dannect.unity.toolkit.py --add-system-methods

# Hello World 메소드 추가 + Git 커밋 (테스트용)
python dannect.unity.toolkit.py --add-hello-world
```

### 6. Git 작업만

```powershell
# Git 커밋만 (푸시 제외)
python dannect.unity.toolkit.py --git-commit

# Git 커밋 + 푸시
python dannect.unity.toolkit.py --git-push
```

---

## 🎯 실전 사용 시나리오

### 시나리오 1: 새 패키지 추가하고 빌드

```powershell
# 1단계: 패키지 추가
python dannect.unity.toolkit.py --package-only

# 2단계: Unity에서 패키지 확인 (수동)

# 3단계: Git 커밋
python dannect.unity.toolkit.py --git-commit

# 4단계: WebGL 빌드
python dannect.unity.toolkit.py --build-only --build-parallel
```

### 시나리오 2: 빠른 빌드 (All-in-One)

```powershell
# 패키지 추가 스킵하고 바로 빌드만
python dannect.unity.toolkit.py --build-only --build-parallel
```

### 시나리오 3: 개발 중 변경사항 커밋

```powershell
# 변경사항 커밋만 (푸시는 나중에)
python dannect.unity.toolkit.py --git-commit

# 나중에 푸시
python dannect.unity.toolkit.py --git-push
```

### 시나리오 4: 디스크 공간 부족할 때

```powershell
# 빌드 출력물 정리 (GB 단위 공간 확보)
python dannect.unity.toolkit.py --clean-builds
```

### 시나리오 5: SystemManager 업데이트

```powershell
# 공통 메소드 추가 (자동 커밋됨)
python dannect.unity.toolkit.py --add-system-methods
```

---

## 📖 옵션 상세 설명

### 기본 옵션

| 옵션 | 설명 | Git 작업 | 빌드 |
|------|------|---------|------|
| (없음) | 패키지 추가만 | ❌ | ❌ |
| `--package-only` | 패키지 추가만 | ❌ | ❌ |
| `--git-commit` | Git 커밋만 (푸시 제외) | ✅ | ❌ |
| `--git-push` | Git 커밋 + 푸시 | ✅ | ❌ |

### 빌드 옵션

| 옵션 | 설명 | 패키지 추가 | Git 작업 | 실행 방식 |
|------|------|------------|---------|----------|
| `--build-webgl` | WebGL 빌드 | ❌ | ❌ | 순차 |
| `--build-webgl --build-parallel` | WebGL 병렬 빌드 | ❌ | ❌ | 병렬 (2개) |
| `--build-only` | 빌드만 (다른 작업 스킵) | ❌ | ❌ | 순차 |
| `--build-only --build-parallel` | 빌드만 (병렬) | ❌ | ❌ | 병렬 (2개) |

### Unity 배치 옵션

| 옵션 | 설명 | 실행 방식 |
|------|------|----------|
| `--unity-batch` | Unity 배치 모드 실행 | 순차 |
| `--unity-batch --parallel` | Unity 배치 모드 병렬 실행 | 병렬 (3개) |

### 기타 옵션

| 옵션 | 설명 | 종료 시점 |
|------|------|----------|
| `--clean-builds` | 빌드 출력물 정리 | 정리 후 종료 |
| `--add-system-methods` | SystemManager 메소드 추가 | 추가 후 즉시 종료 |
| `--add-hello-world` | Hello World 메소드 추가 | 추가 후 즉시 종료 |
| `--help` | 도움말 출력 | 즉시 종료 |

---

## ⚙️ 설정 변경 (config.py)

### WebGL Code Optimization 변경

```python
# Tools/config.py 파일 열기

# Unity 6.0에서 사용 가능한 옵션:
# - "BuildTimes"      : 빠른 빌드 시간 (개발용)
# - "RuntimeSpeed"    : 성능 최적화
# - "RuntimeSpeedLTO" : 성능 최적화 + LTO (최고 성능, 권장) ⭐
# - "DiskSize"        : 크기 최적화
# - "DiskSizeLTO"     : 크기 최적화 + LTO (최소 크기)

WEBGL_CODE_OPTIMIZATION = "RuntimeSpeedLTO"  # 이 값 변경
```

### 프로젝트 경로 변경

```python
# Tools/config.py 파일 열기

# 프로젝트 디렉토리 경로 수정
PROJECT_DIRS = [
    r"C:\경로\프로젝트1",
    r"C:\경로\프로젝트2",
    # ... 추가
]
```

### 빌드 타임아웃 조정

```python
# Tools/config.py 파일 열기

# 빌드 타임아웃 (초) - 프로젝트가 크면 늘리기
BUILD_TIMEOUT = 7200  # 기본 2시간 (7200초)

# Unity 타임아웃 (초)
UNITY_TIMEOUT = 300  # 기본 5분 (300초)
```

---

## 📊 실행 시간 참고

### 작업별 예상 소요 시간

| 작업 | 소요 시간 (프로젝트당) | 비고 |
|------|---------------------|------|
| 패키지 추가 | 1-3초 | manifest.json 수정 |
| Git 커밋 | 2-5초 | 변경사항에 따라 |
| Git 푸시 | 5-15초 | 네트워크 속도에 따라 |
| Unity 배치 모드 | 30초-2분 | 스크립트 복잡도에 따라 |
| WebGL 빌드 (순차) | 5-15분 | 프로젝트 크기에 따라 |
| WebGL 빌드 (병렬) | 3-10분 | 메모리 충분할 때 |

### 전체 프로세스 예상 시간 (3개 프로젝트 기준)

```
패키지 추가 → Git 커밋 → WebGL 빌드 (순차)
= 5초 + 10초 + 45분 = 약 45분

빌드만 (병렬)
= 25분 (최대 2개 동시 빌드)
```

---

## 🔍 로그 확인

### 빌드 로그 위치

```
C:\Users\wkzkx\Desktop\Lim\GitHub\Build\_Logs\

파일명 형식:
프로젝트명_YYYYMMDD_HHMMSS.log

예시:
5.2.1.6_AbioticFactors_20251030_132832.log
```

### 로그 확인 방법

```powershell
# PowerShell에서 최신 로그 확인
cd C:\Users\wkzkx\Desktop\Lim\GitHub\Build\_Logs
Get-ChildItem | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 특정 로그 열기 (VS Code)
code 5.2.1.6_AbioticFactors_20251030_132832.log
```

### 빌드 출력 위치

```
C:\Users\wkzkx\Desktop\Lim\GitHub\Build\프로젝트명\

주요 파일:
- index.html
- 프로젝트명.data
- 프로젝트명.wasm
- 프로젝트명.framework.js
- 프로젝트명.loader.js
```

---

## ❗ 문제 해결 (Troubleshooting)

### 문제 1: Unity 경로를 찾을 수 없습니다

```powershell
# config.py에서 Unity 경로 확인
UNITY_EDITOR_PATH = r"C:\Program Files\Unity\Hub\Editor\6000.0.59f2\Editor\Unity.exe"

# Unity 버전에 맞게 수정 필요
```

### 문제 2: 빌드 타임아웃

```python
# config.py에서 타임아웃 증가
BUILD_TIMEOUT = 10800  # 3시간으로 증가
```

### 문제 3: 메모리 부족 (병렬 빌드 시)

```powershell
# 순차 빌드로 변경
python dannect.unity.toolkit.py --build-only
# --build-parallel 옵션 제거
```

### 문제 4: Git 충돌

```powershell
# 수동으로 충돌 해결 후
python dannect.unity.toolkit.py --git-push
```

### 문제 5: 빌드 실패 확인

```powershell
# 로그 디렉토리에서 실패한 프로젝트 로그 확인
cd C:\Users\wkzkx\Desktop\Lim\GitHub\Build\_Logs
# 에러 메시지 검색
Select-String -Path *.log -Pattern "error|failed|exception" -CaseSensitive
```

---

## 🎓 고급 사용법

### 1. 특정 프로젝트만 빌드

```python
# config.py 수정 (임시)
PROJECT_DIRS = [
    r"C:\경로\빌드할프로젝트",  # 이 프로젝트만 남기기
]

# 빌드 실행
python dannect.unity.toolkit.py --build-only
```

### 2. 다른 Code Optimization으로 빌드

```python
# config.py 수정
WEBGL_CODE_OPTIMIZATION = "DiskSizeLTO"  # 크기 최소화 + LTO

# 빌드 실행
python dannect.unity.toolkit.py --build-only
```

### 3. 여러 작업 순차 실행 (배치 파일)

```batch
@echo off
REM build_all.bat 파일 생성

cd C:\Users\wkzkx\Desktop\Lim\GitHub\SimGround_Package\Tools

echo 1단계: 패키지 추가
python dannect.unity.toolkit.py --package-only

echo 2단계: Git 커밋
python dannect.unity.toolkit.py --git-commit

echo 3단계: WebGL 빌드
python dannect.unity.toolkit.py --build-only --build-parallel

echo 완료!
pause
```

### 4. 빌드 완료 알림 (PowerShell)

```powershell
# 빌드 + 완료 시 소리 알림
python dannect.unity.toolkit.py --build-only
[console]::beep(1000, 500)
Write-Host "빌드 완료!" -ForegroundColor Green
```

---

## 📝 내부 동작 원리 (간단 요약)

### 실행 흐름

```
1. dannect.unity.toolkit.py 실행
   ↓
2. 모든 모듈 import (config, git_utils, unity_cli, ...)
   ↓
3. main() 함수 호출
   ↓
4. 명령행 인수 파싱 (--build-webgl, --parallel 등)
   ↓
5. 옵션에 따라 작업 실행:
   - SystemManager 메소드 추가 (조기 종료)
   - 패키지 추가
   - Git 작업
   - Unity 배치 모드
   - 빌드 정리
   - WebGL 빌드
   ↓
6. 결과 출력 및 종료
```

### Unity 빌드 스크립트 생성 방식

```
1. Python이 C# 스크립트 생성
   Tools/build_manager.py
   → Assets/Editor/AutoWebGLBuildScript.cs
   
2. Unity CLI로 스크립트 실행
   Unity.exe -batchmode -executeMethod AutoWebGLBuildScript.BuildWebGLWithPlayerSettings
   
3. C# 스크립트가 Player Settings 설정 + 빌드
   - Code Optimization 설정 (Il2CppCodeGeneration)
   - 압축, 메모리, 템플릿 등 설정
   - BuildPipeline.BuildPlayer() 호출
```

### Code Optimization 설정 방식

```csharp
// Unity 6.0 API (WasmCodeOptimization)
UnityEditor.WebGL.UserBuildSettings.codeOptimization = WasmCodeOptimization.RuntimeSpeedLTO;

// Unity 6.0에서 사용 가능한 enum 값:
// - WasmCodeOptimization.BuildTimes      : 빠른 빌드 시간
// - WasmCodeOptimization.RuntimeSpeed    : 성능 최적화
// - WasmCodeOptimization.RuntimeSpeedLTO : 성능 최적화 + LTO (권장)
// - WasmCodeOptimization.DiskSize        : 크기 최적화
// - WasmCodeOptimization.DiskSizeLTO     : 크기 최적화 + LTO

// 문서: https://docs.unity3d.com/6000.0/Documentation/ScriptReference/WebGL.WasmCodeOptimization.html
```

---

## 🔗 관련 파일

### 주요 모듈

- `dannect.unity.toolkit.py`: 메인 래퍼 (모든 모듈 import)
- `main.py`: 실행 로직 및 옵션 파싱
- `config.py`: 설정 (경로, 타임아웃, Code Optimization)
- `build_manager.py`: WebGL 빌드 자동화 (Unity 6 전용)
- `git_utils.py`: Git 작업 자동화
- `unity_cli.py`: Unity CLI 실행
- `system_manager.py`: SystemManager 메소드 추가
- `package_manager.py`: manifest.json 패키지 추가

### 생성되는 파일

- `Assets/Editor/AutoWebGLBuildScript.cs`: WebGL 빌드 스크립트 (Unity 6)
- `Assets/Editor/AutoBatchScript.cs`: Unity 배치 모드 스크립트
- `C:\Users\wkzkx\Desktop\Lim\GitHub\Build\_Logs\*.log`: 빌드 로그

---

## 📌 체크리스트

### 빌드 전 확인사항

- [ ] Unity 6 설치 확인
- [ ] `config.py`에서 Unity 경로 확인
- [ ] `config.py`에서 프로젝트 경로 확인
- [ ] `config.py`에서 Code Optimization 설정 확인
- [ ] 빌드 출력 디렉토리 존재 확인
- [ ] 디스크 공간 충분 확인 (프로젝트당 500MB-2GB)

### 빌드 후 확인사항

- [ ] 빌드 로그 확인 (`_Logs` 폴더)
- [ ] 빌드 출력 파일 확인 (index.html, .wasm 등)
- [ ] 브라우저에서 실행 테스트
- [ ] 파일 크기 확인
- [ ] Git 커밋 상태 확인

---

## 📚 추가 참고 자료

### Unity 6 WebGL Build Settings

- Code Optimization: Build Profiles → Web → Code Optimization
- Player Settings: Edit → Project Settings → Player → WebGL
- Build Settings: File → Build Settings

### Python 요구사항

- Python 3.7 이상
- 필요한 라이브러리: subprocess, os, shutil, time, concurrent.futures
- Windows 환경 (PowerShell 또는 CMD)

---

**마지막 업데이트:** 2025-10-30  
**Unity 버전:** Unity 6 (6000.0.59f2)  
**Python 버전:** Python 3.x

