# Dannect Toolkit (`com.dannect.toolkit`)

여러 유니티 프로젝트에서 공용으로 사용하는 프리팹, 자동화, 에디터 스크립트 패키지입니다.

## 주요 기능
- Warning_Pop 등 공용 프리팹 제공
- 프리팹 자동 교체/복사 에디터 스크립트
- MCP, Cursor 등 외부 패키지 의존성 자동 설치
- MCP 서버 자동 실행/설정 스크립트 포함

## 설치 방법

1. 이 패키지를 GitHub에 업로드합니다.
2. 각 프로젝트의 `Packages/manifest.json`에 아래와 같이 추가합니다.

   ```json
   {
     "dependencies": {
       "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
     }
   }
   ```

3. 유니티 에디터를 재시작하면 패키지가 자동으로 설치됩니다.

## 사용법
- Tools > 패키지 프리팹을 프로젝트로 복사 메뉴로 프리팹을 자동 교체할 수 있습니다.
- MCP, Cursor 등 의존성 패키지는 자동으로 설치됩니다.
- MCP 서버 자동 실행/설정은 에디터를 열 때 자동으로 동작합니다.

## 폴더 구조
com.dannect.toolkit/
├─ package.json
├─ README.md
├─ Runtime/
│ ├─ Warning_Pop.prefab
│ ├─ GuideFolder/
│ │ └─ Guide_Pop.prefab
│ └─ Warning_Pop.cs
└─ Editor/
    ├─ PrefabAutoCopier.cs
    └─ MCPServerAutoStart.cs
