import os
import json
import chardet

# =========================
# #region 프로젝트 폴더 및 패키지 정보 (최상단에 위치)
# =========================
project_dirs = [
    r"E:\4.1.2.8_GetWater",
    r"E:\3.1.2.3_AroundAnimals",
    # ... 필요시 추가
]

git_packages = {
    "com.boxqkrtm.ide.cursor": "https://github.com/boxqkrtm/com.unity.ide.cursor.git",
    "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    # 필요시 추가
}
# endregion

# =========================
# #region UTF-8 변환 함수
# =========================
def convert_to_utf8(filepath):
    # 파일의 원래 인코딩 감지
    with open(filepath, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding']
    # 감지된 인코딩으로 읽어서 UTF-8로 저장
    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
# endregion

# =========================
# #region Git 패키지 추가 함수
# =========================
def add_git_packages_to_manifest(project_dir, git_packages):
    manifest_path = os.path.join(project_dir, "Packages", "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"{manifest_path} 없음")
        return

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
# endregion

# =========================
# #region 메인 실행부
# =========================

# 1. UTF-8 변환
for project_dir in project_dirs:
    root_dir = os.path.join(project_dir, "Assets")
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.cs'):
                try:
                    convert_to_utf8(os.path.join(subdir, file))
                    print(f"{file} 변환 완료")
                except Exception as e:
                    print(f"{file} 변환 실패: {e}")

# 2. 각 프로젝트에 패키지 추가
for project_dir in project_dirs:
    add_git_packages_to_manifest(project_dir, git_packages)

# endregion 