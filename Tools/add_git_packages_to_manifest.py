import os
import json

# 수정할 유니티 프로젝트 경로
project_dir = r"E:\4.1.2.8_GetWater"  # ← 실제 프로젝트 경로로 수정

# manifest.json 경로
manifest_path = os.path.join(project_dir, "Packages", "manifest.json")

# 추가/수정할 패키지 정보
git_packages = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.gamelovers.mcp-unity": "https://github.com/CoderGamester/mcp-unity.git"
}

# manifest.json 읽기
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# dependencies에 패키지 추가/수정
for name, url in git_packages.items():
    manifest["dependencies"][name] = url

# manifest.json 저장
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4, ensure_ascii=False)

print("필수 Git 패키지 2종이 manifest.json에 추가/수정되었습니다!")