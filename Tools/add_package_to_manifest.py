import os
import json

# 모든 프로젝트 폴더 리스트
project_dirs = [
    r"E:\Project1",
    r"E:\Project2",
    # ... 추가
]

# 추가할 패키지 정보
package_name = "com.dannect.toolkit"
package_url = "https://github.com/Dannect/SimGround_Package.git#main"

for project_dir in project_dirs:
    manifest_path = os.path.join(project_dir, "Packages", "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"{manifest_path} 없음")
        continue

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # dependencies에 패키지 추가/수정
    manifest["dependencies"][package_name] = package_url

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    print(f"{manifest_path} 수정 완료")