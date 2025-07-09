# Unity 프로젝트 자동화 도구 (dannect.unity.toolkit.py)

Unity 프로젝트의 UTF-8 변환, 패키지 관리, Git 자동화, WebGL 빌드 자동화를 위한 통합 도구입니다.

## 🚀 주요 기능

### 1. C# 파일 UTF-8 변환
- 프로젝트 내 모든 C# 파일을 UTF-8 인코딩으로 자동 변환
- 이미 UTF-8인 파일은 건너뛰어 효율성 확보
- 인코딩 감지 및 안전한 변환 처리

### 2. Unity 패키지 자동 관리
- Git 패키지를 manifest.json에 자동 추가
- 중복 패키지 설치 방지
- 패키지 버전 관리 및 업데이트

### 3. Git 자동화
- 변경사항 자동 감지 및 커밋
- 스마트 브랜치 전략 적용
- 자동 푸시 및 원격 저장소 관리

### 4. Unity WebGL 빌드 자동화
- Unity 6 호환 WebGL 빌드 자동화
- Player Settings 완전 반영 (제품명, 회사명, 버전 등)
- 중앙 집중식 빌드 출력 (`C:\Users\wkzkx\Desktop\Lim\GitHub\Build\`)
- 병렬 빌드 지원으로 빠른 처리
- 과학실험 시뮬레이션 최적화 설정

### 5. Unity 배치 모드
- Unity Editor를 배치 모드로 자동 실행
- 패키지 임포트 및 프로젝트 설정 검증
- 40개 프로젝트 자동 처리 지원
- 병렬 처리로 시간 단축

### 6. Unity 6 호환성
- Unity 6 API 호환성 검사 및 자동 수정
- deprecation 경고 해결
- 최신 Unity 버전 대응

## 📋 시스템 요구사항

- Python 3.6 이상
- Git 설치 및 PATH 설정
- Unity 2021.3 이상 (Unity 6 권장)
- 필요한 Python 패키지:
  ```bash
  pip install chardet
  ```

### Unity 설치 경로
WebGL 빌드를 사용하려면 Unity 설치 경로가 필요합니다:
```
C:\Program Files\Unity\Hub\Editor\6000.0.30f1\Editor\Unity.exe
```

### 메모리 요구사항
- **순차 처리**: 8GB RAM 이상
- **병렬 처리**: 16GB RAM 이상 (권장: 32GB)
- **WebGL 빌드**: 프로젝트당 1GB 디스크 여유공간

## 🔧 설정

### 프로젝트 디렉토리 설정
`dannect.unity.toolkit.py` 파일의 상단에서 프로젝트 경로를 설정합니다:

```python
project_dirs = [
    r"E:\3.1.2.2_ClassifyAnimals",
    r"E:\3.1.2.3_AroundAnimals",
    r"E:\3.1.2.5_UnderWaterAnimals",
    # 새 프로젝트 추가 시 여기에 경로 추가
]
```

### Unity 에디터 경로 설정
Unity CLI 빌드를 위한 Unity 에디터 경로를 설정합니다:

```python
UNITY_EDITOR_PATH = r"C:\Program Files\Unity\Hub\Editor\6000.0.30f1\Editor\Unity.exe"
```

### 빌드 출력 디렉토리 설정
WebGL 빌드 결과물이 저장될 중앙 집중식 출력 폴더를 설정합니다:

```python
BUILD_OUTPUT_DIR = r"C:\Users\wkzkx\Desktop\Lim\GitHub\Build"
```

### Git 패키지 설정
추가할 Git 패키지를 설정합니다:

```python
git_packages = {
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    # 필요한 패키지 추가
}
```

### Git 리포지토리 설정
기본 GitHub 조직 URL을 설정합니다:

```python
GIT_BASE_URL = "https://github.com/Dannect/"
```

## 💻 사용법

### 기본 실행
모든 작업(UTF-8 변환, 패키지 추가, Git 커밋/푸시)을 순차적으로 실행합니다:

```bash
python dannect.unity.toolkit.py
```

### 🚀 자동화 옵션

#### 완전 자동화 (권장)
모든 작업 + Unity 배치 모드를 실행합니다:

```bash
python dannect.unity.toolkit.py --full-auto
```

#### 완전 자동화 + 병렬 처리
빠른 처리를 위해 병렬로 실행합니다:

```bash
python dannect.unity.toolkit.py --full-auto --parallel
```

### 🌐 WebGL 빌드 옵션

#### WebGL 빌드만 실행
Git 작업과 패키지 추가를 제외하고 빌드만 수행합니다:

```bash
python dannect.unity.toolkit.py --build-only
```

#### WebGL 빌드 + 병렬 처리
빠른 빌드를 위해 병렬로 실행합니다:

```bash
python dannect.unity.toolkit.py --build-only --build-parallel
```

#### WebGL 빌드 자동화
전체 작업에 WebGL 빌드를 추가합니다:

```bash
python dannect.unity.toolkit.py --build-webgl
```

### 🔧 Unity 배치 모드 옵션

#### Unity 배치 모드만 실행
Unity Editor를 배치 모드로 실행하여 프로젝트 설정을 검증합니다:

```bash
python dannect.unity.toolkit.py --unity-batch
```

#### 배치 모드 + 병렬 처리
여러 프로젝트를 동시에 처리합니다:

```bash
python dannect.unity.toolkit.py --unity-batch --parallel
```

### 📁 Git 전용 옵션

#### Git 작업만 실행
UTF-8 변환과 패키지 추가를 건너뛰고 Git 작업만 수행합니다:

```bash
python dannect.unity.toolkit.py --git-only
```

#### Git 작업 건너뛰기
UTF-8 변환과 패키지 추가만 수행하고 Git 작업은 건너뜁니다:

```bash
python dannect.unity.toolkit.py --skip-git
```

### 🛠️ 유틸리티 옵션

#### 빌드 출력 정리
중앙 집중식 빌드 출력 폴더를 정리합니다:

```bash
python dannect.unity.toolkit.py --clean-builds
```

#### 도움말 보기
사용법과 옵션을 확인합니다:

```bash
python dannect.unity.toolkit.py --help
```

## 🌿 Git 브랜치 전략

도구는 다음과 같은 스마트 브랜치 전략을 사용합니다:

### 1. 계층구조 최하위 브랜치 우선
- 브랜치 계층구조에서 가장 깊은(아래) 브랜치를 우선 사용
- 커밋 수가 많은 브랜치를 우선 선택
- 커밋 수가 같으면 최근에 작업된 브랜치 선택
- `main` 브랜치는 제외

### 2. dev 브랜치 보조 사용
- 다른 브랜치가 없으면 `dev` 브랜치 사용

### 3. dev 브랜치 자동 생성
- `dev` 브랜치도 없으면 `dev` 브랜치를 새로 생성

### 브랜치 선택 예시
```
브랜치 분석:
  main: 10개 커밋
  feature-base: 15개 커밋
  feature-ui: 20개 커밋 (feature-base에서 파생)
  feature-ui-detail: 25개 커밋 (feature-ui에서 파생)
→ feature-ui-detail 브랜치 선택 (가장 깊은 계층)

브랜치 목록: main, dev
→ dev 브랜치 선택

브랜치 목록: main
→ dev 브랜치 새로 생성
```

## 🌐 리포지토리 URL 자동 생성

프로젝트 폴더명을 기반으로 GitHub 리포지토리 URL을 자동 생성합니다:

| 프로젝트 경로 | 생성되는 리포지토리 URL |
|---------------|------------------------|
| `E:\3.1.2.2_ClassifyAnimals` | `https://github.com/Dannect/3.1.2.2_ClassifyAnimals` |
| `E:\3.1.2.3_AroundAnimals` | `https://github.com/Dannect/3.1.2.3_AroundAnimals` |
| `E:\3.1.2.5_UnderWaterAnimals` | `https://github.com/Dannect/3.1.2.5_UnderWaterAnimals` |

## 📁 프로젝트 구조

```
SimGround_Package/
├── Tools/
│   ├── dannect.unity.toolkit.py         # 메인 스크립트
│   ├── Unity_Batch_Guide.md            # Unity 배치 모드 가이드
│   ├── unity6_compatibility_report.md  # Unity 6 호환성 보고서
│   └── validate_commit_messages.py     # 커밋 메시지 검증 도구
├── Editor/
│   ├── Dannect.Toolkit.Editor.asmdef   # Editor 어셈블리 정의
│   └── Scripts/                        # Editor 스크립트 (PackageAssetCopier 제거됨)
├── Runtime/
│   ├── Dannect.Toolkit.Runtime.asmdef  # Runtime 어셈블리 정의
│   ├── Prefabs/
│   │   └── Warning_Pop.prefab          # 경고 팝업 프리팹
│   └── Scripts/                        # Runtime 스크립트
├── package.json                        # Unity 패키지 정의
└── README.md                           # 이 파일
```

## 🔍 작업 흐름

### 1. UTF-8 변환 단계
```
프로젝트 폴더 스캔
    ↓
Assets 폴더 내 .cs 파일 검색
    ↓
인코딩 감지 및 UTF-8 변환
    ↓
변환 결과 출력
```

### 2. 패키지 추가 단계
```
manifest.json 파일 확인
    ↓
기존 패키지와 비교
    ↓
새 패키지 추가/업데이트
    ↓
manifest.json 저장
```

### 3. Git 자동화 단계
```
Git 리포지토리 확인/초기화
    ↓
변경사항 감지
    ↓
대상 브랜치 결정
    ↓
브랜치 체크아웃/생성
    ↓
스테이징 → 커밋 → 푸시
```

### 4. Unity 배치 모드 단계
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

### 5. WebGL 빌드 단계
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

### 6. Unity 6 호환성 검사 단계
```
프로젝트 스캔
    ↓
deprecated API 패턴 검색
    ↓
Unity 6 호환 코드로 자동 변환
    ↓
호환성 보고서 생성
```

## 🛡️ 안전성 기능

### 에러 처리
- 각 Git 명령어의 성공/실패 체크
- 파일 인코딩 변환 시 예외 처리
- 존재하지 않는 폴더 건너뛰기

### 중복 작업 방지
- 이미 UTF-8인 파일 변환 건너뛰기
- 기존 패키지 중복 설치 방지
- 변경사항이 없는 경우 커밋 건너뛰기

### 자동 초기화
- Git 리포지토리 자동 초기화
- 원격 저장소 자동 설정
- 브랜치 자동 생성

## 📝 로그 출력 예시

### 완전 자동화 모드 (--full-auto)
```
=== Unity 프로젝트 자동화 도구 시작 ===

1. C# 파일 UTF-8 변환 작업 시작...

--- 6.1.4.5_ConvexLensLight UTF-8 변환 ---
  LensController.cs 변환 완료
  LightManager.cs 이미 UTF-8, 변환 생략

2. Unity 패키지 추가 작업 시작...

--- 6.1.4.5_ConvexLensLight 패키지 추가 ---
E:\6.1.4.5_ConvexLensLight\Packages\manifest.json에 패키지들 추가/수정 완료!

3. Git 커밋 및 푸시 작업 시작...

=== 6.1.4.5_ConvexLensLight Git 작업 시작 ===
변경사항 발견: 6.1.4.5_ConvexLensLight
브랜치 계층 분석 중...
  feature-base: 15개 커밋, 최근 커밋: 1703123456
  feature-ui: 20개 커밋, 최근 커밋: 1703125678
계층구조에서 가장 깊은 브랜치 사용: feature-ui
브랜치 체크아웃: feature-ui
커밋 완료: 6.1.4.5_ConvexLensLight
푸시 완료: 6.1.4.5_ConvexLensLight -> feature-ui
=== 6.1.4.5_ConvexLensLight Git 작업 완료 ===

4. Unity 배치 모드 작업 시작...

=== 6.1.4.5_ConvexLensLight Unity 배치 처리 시작 ===
Unity 배치 스크립트 생성 완료
Unity CLI 배치 모드 실행 중...
패키지 임포트 및 Asset Database 갱신 완료
프로젝트 설정 검증 완료
✅ 6.1.4.5_ConvexLensLight Unity 배치 처리 완료

=== 모든 작업 완료 ===
```

### WebGL 빌드 모드 (--build-only)
```
=== Unity 프로젝트 자동화 도구 시작 ===

WebGL 빌드만 실행합니다 (Git 작업 및 패키지 추가 제외)...

5. Unity WebGL 프로젝트 빌드 시작...
🌐 빌드 타겟: WebGL
📊 총 2개 프로젝트 빌드 예정

=== 6.1.4.5_ConvexLensLight WebGL 빌드 시작 ===
🌐 Unity WebGL Player Settings 반영 빌드 시작: 6.1.4.5_ConvexLensLight
빌드 출력 디렉토리 생성: C:\Users\wkzkx\Desktop\Lim\GitHub\Build\6.1.4.5_ConvexLensLight
Unity WebGL 빌드 스크립트 생성 완료
Unity CLI WebGL 빌드 실행 중...
✅ 6.1.4.5_ConvexLensLight WebGL 빌드 완료 (14초, 65MB)

=== 6.1.4.6_ConvexLensObservation WebGL 빌드 시작 ===
🌐 Unity WebGL Player Settings 반영 빌드 시작: 6.1.4.6_ConvexLensObservation
빌드 출력 디렉토리 생성: C:\Users\wkzkx\Desktop\Lim\GitHub\Build\6.1.4.6_ConvexLensObservation
Unity WebGL 빌드 스크립트 생성 완료
Unity CLI WebGL 빌드 실행 중...
✅ 6.1.4.6_ConvexLensObservation WebGL 빌드 완료 (15초, 68MB)

🎉 WebGL 빌드 완료!
✅ 성공: 2개 프로젝트
📁 빌드 출력: C:\Users\wkzkx\Desktop\Lim\GitHub\Build\
```

## 🚨 주의사항

1. **Git 인증**: GitHub에 대한 적절한 인증 설정이 필요합니다 (SSH 키 또는 Personal Access Token)
2. **권한**: 대상 리포지토리에 대한 푸시 권한이 있어야 합니다
3. **백업**: 중요한 변경사항이 있는 경우 수동 백업을 권장합니다
4. **네트워크**: 인터넷 연결이 필요합니다 (Git 푸시 작업)
5. **Unity 경로**: Unity 설치 경로가 올바르게 설정되어 있어야 합니다
6. **메모리**: WebGL 빌드 시 충분한 메모리가 필요합니다 (프로젝트당 2-4GB)
7. **디스크 공간**: 빌드 출력 디렉토리에 충분한 여유 공간이 있어야 합니다
8. **Unity 버전**: Unity 6 사용 권장 (Unity 2021.3 이상 지원)

## 🔧 문제 해결

### Git 인증 오류
```bash
# SSH 키 설정 확인
ssh -T git@github.com

# 또는 HTTPS 인증 설정
git config --global credential.helper store
```

### 인코딩 감지 오류
```bash
# chardet 패키지 재설치
pip uninstall chardet
pip install chardet
```

### Unity 경로 오류
```bash
# Unity 설치 경로 확인
dir "C:\Program Files\Unity\Hub\Editor\"

# 또는 자동 검색 기능 사용
python dannect.unity.toolkit.py --help
```

### WebGL 빌드 실패
```bash
# Unity 로그 확인
type "%USERPROFILE%\AppData\Local\Unity\Editor\Editor.log"

# 메모리 부족 시 순차 빌드 사용
python dannect.unity.toolkit.py --build-only
```

### 병렬 처리 오류
```bash
# 병렬 처리 수 조정 (메모리 부족 시)
# dannect.unity.toolkit.py에서 MAX_WORKERS 값 조정

# 또는 순차 처리 사용
python dannect.unity.toolkit.py --build-webgl
```

### Unity 배치 모드 실패
```bash
# Unity 프로젝트 무결성 확인
# Unity Editor로 프로젝트 열어서 오류 확인

# 또는 개별 프로젝트 처리
python dannect.unity.toolkit.py --unity-batch --project-path "경로"
```

### 권한 오류
- 프로젝트 폴더에 대한 읽기/쓰기 권한 확인
- Git 리포지토리에 대한 푸시 권한 확인
- Unity 설치 폴더에 대한 실행 권한 확인

## 📞 지원

문제가 발생하거나 기능 요청이 있는 경우:
1. GitHub Issues를 통해 문의
2. 로그 출력 내용과 함께 상세한 오류 상황 제공
3. Unity 버전 및 시스템 환경 정보 포함

## 🔄 업데이트 내역

### v2.0.0 (2025년)
- Unity WebGL 빌드 자동화 추가
- Unity 배치 모드 지원
- Unity 6 호환성 검사 기능
- 병렬 처리 지원
- 중앙 집중식 빌드 출력
- PackageAssetCopier 기능 대체 (프로젝트 설정 검증)

### v1.0.0 (2024년)
- UTF-8 변환 기능
- Unity 패키지 자동 관리
- Git 자동화 기능
- 스마트 브랜치 전략

## 📄 라이선스

이 도구는 교육 목적으로 개발되었습니다.

---

**개발자**: 임주영  
**버전**: 2.0.0  
**최종 업데이트**: 2025년 1월  
**지원 Unity 버전**: Unity 2021.3 이상 (Unity 6 권장)  
**지원 플랫폼**: WebGL, Editor 
