"""
패키지 관리 관련 함수들
"""
import os
import json
from config import Config

# 전역 변수 참조 (호환성 유지)
git_packages = Config.GIT_PACKAGES


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

