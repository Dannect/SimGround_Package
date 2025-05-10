import os
import json

# 모든 프로젝트 폴더 리스트
project_dirs = [
    r"E:\4.1.2.8_GetWater",
    
    # ... 추가
]

# 여러 Git 패키지 정보 (패키지명: Git 주소)
git_packages = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    #"com.gamelovers.mcp-unity": "https://github.com/CoderGamester/mcp-unity.git",
    # ... 추가
}

# 각 프로젝트에 대해 반복
for project_dir in project_dirs:
    manifest_path = os.path.join(project_dir, "Packages", "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"{manifest_path} 없음")
        continue

    # manifest.json 파일 열기
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # 모든 Git 패키지 추가/수정
    for name, url in git_packages.items():
        manifest["dependencies"][name] = url

    # manifest.json 파일 저장
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    print(f"{manifest_path}에 패키지들 추가 완료!")
