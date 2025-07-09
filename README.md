# Unity 프로젝트 자동화 도구 (dannect.unity.toolkit.py)

Unity 프로젝트의 패키지 관리, Git 자동화, WebGL 빌드 자동화를 위한 통합 도구입니다.

## 🚀 주요 기능

### 1. Unity 패키지 자동 관리
- Git 패키지를 manifest.json에 자동 추가
- 중복 패키지 설치 방지
- 패키지 버전 관리 및 업데이트

### 2. Git 자동화 시스템
- 스마트 브랜치 전략 (계층구조 기반 브랜치 선택)
- 변경사항 자동 감지 및 커밋
- Git 인덱스 문제 자동 해결
- 브랜치 자동 생성 및 체크아웃
- 커밋과 푸시 분리 실행 지원

### 3. Unity WebGL 빌드 자동화
- Unity WebGL 빌드 자동화
- Player Settings 완전 반영 (제품명, 회사명, 버전, WebGL 설정)
- 중앙 집중식 빌드 출력 (`C:\Users\wkzkx\Desktop\Lim\GitHub\Build\`)
- 병렬 빌드 지원으로 빠른 처리 (최대 2개 동시)
- 과학실험 시뮬레이션 최적화 설정

### 4. Unity 배치 모드 자동화
- Unity Editor를 배치 모드로 자동 실행
- 패키지 임포트 및 Asset Database 갱신
- 프로젝트 설정 검증 및 자동 스크립트 생성
- 병렬 처리 지원 (최대 3개 동시)
- GUI 없이 백그라운드 실행

### 5. SystemManager 메소드 관리
- SystemManager.cs 파일 자동 탐색
- 공통 메소드 자동 추가 (AllowKeyboardInput 등)
- Hello World 메소드 추가 및 Start() 호출 설정
- 메소드 중복 확인 및 안전한 추가

### 6. 빌드 출력물 관리
- 중앙 집중식 빌드 폴더 정리
- 프로젝트별 빌드 출력 크기 표시
- 디스크 공간 효율적 관리

## 📋 시스템 요구사항

### 기본 요구사항
- **Python**: 3.6 이상
- **Git**: 설치 및 PATH 설정 필요
- **Unity**: 2021.3 이상
- **OS**: Windows 10/11

### Unity 설치 경로
WebGL 빌드를 사용하려면 Unity 설치 경로가 필요합니다:
```
C:\Program Files\Unity\Hub\Editor\6000.0.30f1\Editor\Unity.exe
```

### 메모리 요구사항
- **순차 처리**: 8GB RAM 이상
- **병렬 처리**: 16GB RAM 이상 (권장: 32GB)
- **WebGL 빌드**: 프로젝트당 2-4GB 메모리 및 1GB 디스크 여유공간

### 네트워크 요구사항
- Git 패키지 다운로드를 위한 인터넷 연결
- GitHub 접근을 위한 Git 인증 설정 (SSH 키 또는 Personal Access Token)

## 🔧 설정

### 1. 프로젝트 디렉토리 설정
`dannect.unity.toolkit.py` 파일의 `Config` 클래스에서 프로젝트 경로를 설정합니다:

```python
class Config:
    PROJECT_DIRS = [
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.5_ConvexLensLight",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.6_ConvexLensObservation",
        # 새 프로젝트 추가 시 여기에 경로 추가
    ]
```

### 2. Unity 에디터 경로 설정
Unity CLI 빌드를 위한 Unity 에디터 경로:

```python
UNITY_EDITOR_PATH = r"C:\Program Files\Unity\Hub\Editor\6000.0.30f1\Editor\Unity.exe"
```

### 3. 빌드 출력 디렉토리 설정
WebGL 빌드 결과물이 저장될 중앙 집중식 출력 폴더:

```python
BUILD_OUTPUT_DIR = r"C:\Users\wkzkx\Desktop\Lim\GitHub\Build"
```

### 4. Git 패키지 설정
추가할 Git 패키지 목록:

```python
GIT_PACKAGES = {
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
}
```

### 5. Git 리포지토리 설정
기본 GitHub 조직 URL:

```python
GIT_BASE_URL = "https://github.com/Dannect/"
DEFAULT_BRANCH = "main"
DEV_BRANCH = "dev"
```

## 💻 사용법

### 기본 실행 (패키지 추가만)
```bash
python dannect.unity.toolkit.py
```

### 📦 패키지 관리 옵션

#### 패키지 추가만 실행
```bash
python dannect.unity.toolkit.py --package-only
```

### 🌿 Git 작업 옵션

#### Git 커밋 및 푸시
```bash
python dannect.unity.toolkit.py --git-push
```

#### Git 커밋만 (푸시 제외)
```bash
python dannect.unity.toolkit.py --git-commit
```

### 🔧 Unity 배치 모드 옵션

#### Unity 배치 모드 실행
```bash
python dannect.unity.toolkit.py --unity-batch
```

#### 병렬 배치 모드 실행 (3개 동시)
```bash
python dannect.unity.toolkit.py --unity-batch --parallel
```

### 🌐 WebGL 빌드 옵션

#### WebGL 빌드 자동화
```bash
python dannect.unity.toolkit.py --build-webgl
```

#### WebGL 빌드 + 병렬 처리 (2개 동시)
```bash
python dannect.unity.toolkit.py --build-webgl --build-parallel
```

#### WebGL 빌드만 실행 (Git 작업 제외)
```bash
python dannect.unity.toolkit.py --build-only
```

#### 빌드 출력물 정리
```bash
python dannect.unity.toolkit.py --clean-builds
```



### 🛠️ SystemManager 메소드 관리

#### 공통 메소드 추가 (AllowKeyboardInput 등)
```bash
python dannect.unity.toolkit.py --add-system-methods
```

#### Hello World 메소드 추가
```bash
python dannect.unity.toolkit.py --add-hello-world
```

### 📖 도움말
```bash
python dannect.unity.toolkit.py --help
```

## 🌿 Git 브랜치 전략

도구는 다음과 같은 스마트 브랜치 전략을 사용합니다:

### 1. 브랜치 계층구조 기반 선택
- 브랜치 계층구조에서 가장 깊은(하위) 브랜치를 우선 사용
- 커밋 수가 많은 브랜치를 우선 선택
- 커밋 수가 같으면 최근에 작업된 브랜치 선택
- `main` 브랜치는 선택 대상에서 제외

### 2. dev 브랜치 보조 사용
- 적절한 하위 브랜치가 없으면 `dev` 브랜치 사용

### 3. dev 브랜치 자동 생성
- `dev` 브랜치도 없으면 자동으로 생성하여 사용

### 브랜치 선택 예시
```
브랜치 분석 결과:
  main: 10개 커밋 (제외)
  feature-base: 15개 커밋, 최근 커밋: 1703123456
  feature-ui: 20개 커밋, 최근 커밋: 1703125678
  feature-ui-detail: 25개 커밋, 최근 커밋: 1703127890
→ feature-ui-detail 브랜치 선택 (가장 많은 커밋 수)

브랜치 목록: main, dev
→ dev 브랜치 선택

브랜치 목록: main
→ dev 브랜치 새로 생성
```

## 🌐 리포지토리 URL 자동 생성

프로젝트 폴더명을 기반으로 GitHub 리포지토리 URL을 자동 생성합니다:

| 프로젝트 경로 | 생성되는 리포지토리 URL |
|---------------|------------------------|
| `C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.5_ConvexLensLight` | `https://github.com/Dannect/6.1.4.5_ConvexLensLight` |
| `C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.6_ConvexLensObservation` | `https://github.com/Dannect/6.1.4.6_ConvexLensObservation` |

## 📁 프로젝트 구조

```
SimGround_Package/
├── Tools/
│   ├── dannect.unity.toolkit.py         # 메인 자동화 스크립트
│   ├── Unity_Batch_Guide.md            # Unity 배치 모드 사용 가이드

│   └── validate_commit_messages.py     # 커밋 메시지 검증 도구
├── Editor/
│   ├── Dannect.Toolkit.Editor.asmdef   # Editor 어셈블리 정의
│   └── Scripts/                        # Editor 스크립트
├── Runtime/
│   ├── Dannect.Toolkit.Runtime.asmdef  # Runtime 어셈블리 정의
│   ├── Prefabs/                        # Runtime 프리팹
│   └── Scripts/                        # Runtime 스크립트
├── package.json                        # Unity 패키지 정의
└── README.md                           # 이 파일
```

## 🔍 상세 기능 설명

### 1. Unity 패키지 자동 관리
```
manifest.json 파일 확인
    ↓
기존 패키지와 비교
    ↓
새 패키지 추가/업데이트
    ↓
manifest.json 저장
```

### 2. Git 자동화 시스템
```
Git 리포지토리 확인/초기화
    ↓
Git 상태 확인 및 문제 해결
    ↓
변경사항 감지
    ↓
대상 브랜치 결정 (계층구조 분석)
    ↓
브랜치 체크아웃/생성
    ↓
스테이징 → 커밋 → 푸시 (선택적)
```

### 3. Unity 배치 모드 자동화
```
Unity 배치 스크립트 생성
    ↓
Unity CLI 배치 모드 실행
    ↓
패키지 임포트 및 Asset Database 갱신
    ↓
프로젝트 설정 검증
    ↓
최종 Asset Database 저장
```

### 4. Unity WebGL 빌드 자동화
```
Unity WebGL 빌드 스크립트 생성
    ↓
Player Settings 자동 설정
    ↓
빌드 출력 디렉토리 생성
    ↓
Unity CLI WebGL 빌드 실행
    ↓
중앙 집중식 빌드 출력 저장
```

### 5. SystemManager 메소드 관리
```
SystemManager.cs 파일 탐색
    ↓
클래스 구조 분석
    ↓
메소드 존재 여부 확인
    ↓
메소드 추가 (클래스 마지막 위치)
    ↓
Start() 메소드 호출 추가 (Hello World 전용)
```

## 🛡️ 안전성 기능

### 에러 처리 및 복구
- 각 Git 명령어의 성공/실패 상태 확인
- Git 인덱스 문제 자동 감지 및 해결
- Unity 경로 자동 검색 (설정 경로 없을 시)
- 존재하지 않는 프로젝트 폴더 자동 건너뛰기

### 중복 작업 방지
- 기존 패키지 중복 설치 방지
- 변경사항이 없는 경우 Git 커밋 건너뛰기
- 이미 존재하는 메소드 추가 방지
- 동일한 API 수정 중복 방지

### 자동 초기화 및 설정
- Git 리포지토리 자동 초기화
- 원격 저장소 자동 설정
- 브랜치 자동 생성 및 체크아웃
- Unity 배치 스크립트 자동 생성

## 📝 실행 예시

### 패키지 추가 모드
```bash
$ python dannect.unity.toolkit.py --package-only

=== Unity 프로젝트 자동화 도구 시작 ===
패키지 추가만 실행합니다 (Git 작업 제외)...

--- 6.1.4.5_ConvexLensLight 패키지 추가 ---
C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.5_ConvexLensLight\Packages\manifest.json에 패키지들 추가/수정 완료!

--- 6.1.4.6_ConvexLensObservation 패키지 추가 ---
com.dannect.toolkit 이미 설치됨, 생략

=== 모든 작업 완료 ===
```

### Git 커밋 및 푸시 모드
```bash
$ python dannect.unity.toolkit.py --git-push

=== Unity 프로젝트 자동화 도구 시작 ===
Git 커밋 및 푸시만 실행합니다 (패키지 추가 제외)...

=== 6.1.4.5_ConvexLensLight Git 커밋 시작 ===
📝 커밋 메시지: FEAT: Unity 패키지 업데이트 및 자동 설정 적용
변경사항 발견: 6.1.4.5_ConvexLensLight
브랜치 계층 분석 중...
  feature-ui: 20개 커밋, 최근 커밋: 1703125678
계층구조에서 가장 깊은 브랜치 사용: feature-ui
브랜치 체크아웃: feature-ui
브랜치 'feature-ui'로 체크아웃 완료
커밋 완료: 6.1.4.5_ConvexLensLight
=== 6.1.4.5_ConvexLensLight Git 커밋 완료 ===

=== 6.1.4.5_ConvexLensLight Git 푸시 시작 ===
현재 브랜치: feature-ui
푸시할 커밋 발견: 1개
푸시 완료: 6.1.4.5_ConvexLensLight -> feature-ui
=== 6.1.4.5_ConvexLensLight Git 푸시 완료 ===

=== 모든 작업 완료 ===
```

### Unity 배치 모드 병렬 실행
```bash
$ python dannect.unity.toolkit.py --unity-batch --parallel

=== Unity 프로젝트 자동화 도구 시작 ===
Unity 배치 모드만 실행합니다...

=== 병렬 처리 시작 (최대 3개 동시 실행) ===
배치 스크립트 생성 중...
배치 스크립트 생성 완료: C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.5_ConvexLensLight\Assets\Editor\BatchScripts\AutoBatchProcessor.cs

=== 6.1.4.5_ConvexLensLight Unity 배치 처리 시작 ===
Unity 배치 모드 실행 중: 6.1.4.5_ConvexLensLight
Unity 명령어: C:\Program Files\Unity\Hub\Editor\6000.0.30f1\Editor\Unity.exe -batchmode -quit -projectPath C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.5_ConvexLensLight -logFile -

=== Unity 출력 ===
[Log] === 배치 처리 시작 ===
[Log] 프로젝트 설정 검증 중...
[Log] 프로젝트 설정 검증 완료
[Log] === 배치 처리 완료 ===

✅ 6.1.4.5_ConvexLensLight 병렬 처리 완료
✅ 6.1.4.6_ConvexLensObservation 병렬 처리 완료

=== 병렬 처리 결과 ===
성공: 2개
실패: 0개
총 처리: 2개

=== 모든 작업 완료 ===
```

### WebGL 빌드 모드
```bash
$ python dannect.unity.toolkit.py --build-webgl --build-parallel

=== Unity 프로젝트 자동화 도구 시작 ===

5. Unity WebGL 프로젝트 빌드 시작...
🌐 빌드 타겟: WebGL
📊 총 2개 프로젝트 빌드 예정
🎯 WebGL Player Settings 완전 반영 빌드 모드
📚 과학실험 시뮬레이션 최적화 적용

🌐 WebGL 병렬 빌드 시작 (최대 2개 동시 실행)

🌐 Unity WebGL Player Settings 반영 빌드 시작: 6.1.4.5_ConvexLensLight
빌드 출력 디렉토리 생성: C:\Users\wkzkx\Desktop\Lim\GitHub\Build\6.1.4.5_ConvexLensLight
WebGL 전용 빌드 스크립트 생성 완료
🌐 Unity WebGL 빌드 실행 중... (타임아웃: 1800초)

=== Unity WebGL 빌드 로그 ===
[Log] === WebGL Player Settings 자동 설정 및 빌드 시작 ===
[Log] 🔧 WebGL Player Settings 이미지 기반 고정 설정 적용 중...
[Log] ✅ 제품명 설정: Science Experiment Simulation
[Log] ✅ 해상도 설정: 1655x892, Run In Background 활성화
[Log] ✅ WebGL 템플릿 설정: Minimal
[Log] ✅ Publishing Settings: 압축 비활성화, 프로젝트명 기반 파일명, 데이터 캐싱 활성화
[Log] ✅ WebGL 빌드 성공!
[Log] 📦 빌드 크기: 45.2 MB
[Log] ⏱️ 빌드 시간: 00:00:14

✅ 6.1.4.5_ConvexLensLight WebGL 병렬 빌드 완료
✅ 6.1.4.6_ConvexLensObservation WebGL 병렬 빌드 완료

=== WebGL 병렬 빌드 결과 ===
성공: 2개
실패: 0개
총 빌드: 2개

=== 최종 WebGL 빌드 결과 ===
✅ 성공: 2개
❌ 실패: 0개
📊 총 빌드: 2개

🌐 WebGL 빌드 완료된 프로젝트들:
  - 6.1.4.5_ConvexLensLight
  - 6.1.4.6_ConvexLensObservation

=== 모든 작업 완료 ===
```



## 🚨 주의사항

### 1. Git 인증 설정
- GitHub에 대한 적절한 인증 설정이 필요합니다 (SSH 키 또는 Personal Access Token)
- 대상 리포지토리에 대한 푸시 권한이 있어야 합니다

### 2. Unity 설정
- Unity 설치 경로가 올바르게 설정되어 있어야 합니다
- Unity 2021.3 이상 지원
- WebGL 빌드 모듈이 설치되어 있어야 합니다

### 3. 시스템 리소스
- WebGL 빌드 시 충분한 메모리가 필요합니다 (프로젝트당 2-4GB)
- 병렬 처리 시 시스템 리소스 사용량이 증가합니다
- 빌드 출력 디렉토리에 충분한 여유 공간이 있어야 합니다

### 4. 네트워크 연결
- 인터넷 연결이 필요합니다 (Git 푸시 및 패키지 다운로드)
- 방화벽 설정이 Git 및 Unity 통신을 허용해야 합니다

### 5. 백업 및 복원
- 중요한 변경사항이 있는 경우 수동 백업을 권장합니다
- Git 커밋 전 프로젝트 상태를 확인해주세요

## 🔧 문제 해결

### Git 관련 문제

#### Git 인증 오류
```bash
# SSH 키 설정 확인
ssh -T git@github.com

# HTTPS 인증 설정
git config --global credential.helper store
```

#### Git 인덱스 문제
- 도구에 자동 해결 기능이 포함되어 있습니다
- `git reset --hard HEAD`로 수동 해결 가능

#### 브랜치 체크아웃 실패
- 도구가 자동으로 Git 상태를 정리하고 재시도합니다
- 수동으로 `git clean -fd`로 untracked 파일 제거 가능

### Unity 관련 문제

#### Unity 경로 오류
```bash
# Unity 설치 경로 확인
dir "C:\Program Files\Unity\Hub\Editor\"

# 도구의 자동 검색 기능 사용
python dannect.unity.toolkit.py --help
```

#### WebGL 빌드 실패
```bash
# Unity 로그 확인
type "%USERPROFILE%\AppData\Local\Unity\Editor\Editor.log"

# 메모리 부족 시 순차 빌드 사용
python dannect.unity.toolkit.py --build-only
```

#### 배치 모드 실패
- Unity 프로젝트 무결성 확인
- Unity Editor로 프로젝트를 열어 오류 확인
- 개별 프로젝트 처리 시도

### 시스템 리소스 문제

#### 메모리 부족
```bash
# 병렬 처리 수 조정
# Config 클래스의 max_workers 값 조정

# 순차 처리 사용
python dannect.unity.toolkit.py --build-webgl
```

#### 디스크 공간 부족
```bash
# 빌드 출력물 정리
python dannect.unity.toolkit.py --clean-builds

# 임시 파일 정리
# Unity 캐시 폴더 정리
```

### 권한 문제
- 프로젝트 폴더에 대한 읽기/쓰기 권한 확인
- Git 리포지토리에 대한 푸시 권한 확인
- Unity 설치 폴더에 대한 실행 권한 확인
- 관리자 권한으로 실행 시도

## 📞 지원 및 문의

문제가 발생하거나 기능 요청이 있는 경우:

1. **GitHub Issues**: 버그 리포트 및 기능 요청
2. **로그 정보**: 오류 발생 시 전체 로그 출력 내용 제공
3. **환경 정보**: Unity 버전, Python 버전, OS 정보 포함
4. **재현 단계**: 문제 재현을 위한 단계별 설명

### 로그 수집 방법
```bash
# 상세 로그와 함께 실행
python dannect.unity.toolkit.py --build-webgl > build_log.txt 2>&1

# 로그 파일 확인
type build_log.txt
```

## 🔄 업데이트 내역

### v3.0.0 (2025년 1월)
- SystemManager 메소드 자동 관리 기능 추가
- Git 브랜치 계층구조 분석 기능 강화
- WebGL 빌드 Player Settings 완전 반영
- Unity 배치 모드 병렬 처리 최적화
- 빌드 출력물 중앙 집중식 관리

### v2.0.0 (2024년)
- Unity WebGL 빌드 자동화 추가
- Unity 배치 모드 지원
- 병렬 처리 지원
- 중앙 집중식 빌드 출력
- Git 자동화 시스템 개선

### v1.0.0 (2024년 초)
- Unity 패키지 자동 관리 기능
- 기본 Git 자동화 기능
- 브랜치 전략 시스템

## 📊 성능 벤치마크

### 처리 시간 (프로젝트당)
- **패키지 추가**: 1-3초
- **Git 커밋**: 5-10초
- **Unity 배치 모드**: 30-60초
- **WebGL 빌드**: 300-900초 (5-15분)

### 병렬 처리 효과
- **Unity 배치 모드**: 3배 빠름 (3개 동시 처리)
- **WebGL 빌드**: 2배 빠름 (2개 동시 처리)
- **메모리 사용량**: 2-4배 증가

### 디스크 사용량
- **WebGL 빌드 출력**: 프로젝트당 50-200MB
- **Unity 캐시**: 프로젝트당 100-500MB
- **전체 빌드 폴더**: 2-10GB (모든 프로젝트)

## 📄 라이선스

이 도구는 교육 목적으로 개발되었으며, Unity 과학실험 시뮬레이션 프로젝트 자동화에 특화되어 있습니다.

---

**개발자**: 임주영  
**버전**: 3.0.0  
**최종 업데이트**: 2025년 1월  
**지원 Unity 버전**: Unity 2021.3 이상  
**지원 플랫폼**: WebGL, Editor  
**지원 언어**: 한국어  
**개발 환경**: Windows 10/11, Python 3.6+ 
