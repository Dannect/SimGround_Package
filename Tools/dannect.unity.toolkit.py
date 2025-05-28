import os
import json
import chardet

# =========================
# #region 프로젝트 폴더 및 패키지 정보 (최상단에 위치)
# =========================
project_dirs = [
<<<<<<< Updated upstream
    r"E:\3.1.2.2_ClassifyAnimals",
    r"E:\3.1.2.3_AroundAnimals",
    r"E:\4.1.2.8_GetWater",
    # ... 필요시 추가
=======
    r"E:\5.1.3.3_Experiment",
    r"E:\TDS",
    # 40개 프로젝트 경로를 여기에 추가하세요
    # 예시:
    # r"E:\Project1",
    # r"E:\Project2",
    # r"E:\Project3",
    # ... 계속 추가
    
    # 자동 스캔 기능을 원한다면 아래 함수를 사용하세요
    # get_unity_projects_from_directory(r"E:\UnityProjects")
>>>>>>> Stashed changes
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
    # 이미 UTF-8이면 변환하지 않음
    if encoding and encoding.lower().replace('-', '') == 'utf8':
        return False  # 변환하지 않음
    # 감지된 인코딩으로 읽어서 UTF-8로 저장
    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True  # 변환함
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

    changed = False  # 변경 여부 플래그

    # 모든 Git 패키지 추가/수정
    for name, url in git_packages.items():
        # 이미 동일한 값이 있으면 건너뜀
        if name in manifest["dependencies"] and manifest["dependencies"][name] == url:
            print(f"{name} 이미 설치됨, 생략")
            continue
        manifest["dependencies"][name] = url
        changed = True

    # 변경된 경우에만 저장
    if changed:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
        print(f"{manifest_path}에 패키지들 추가/수정 완료!")
    else:
        print(f"{manifest_path} 변경 없음 (모든 패키지 이미 설치됨)")
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
                    changed = convert_to_utf8(os.path.join(subdir, file))
                    if changed:
                        print(f"{file} 변환 완료")
                    else:
                        print(f"{file} 이미 UTF-8, 변환 생략")
                except Exception as e:
                    print(f"{file} 변환 실패: {e}")

# 2. 각 프로젝트에 패키지 추가
for project_dir in project_dirs:
    add_git_packages_to_manifest(project_dir, git_packages)

# endregion 