"""
Unity 프로젝트 자동화 도구 - 리팩토링된 버전 (모듈화)
원본 파일은 호환성을 위해 래퍼 역할을 수행하며, 모든 기능은 모듈화된 파일들에서 import합니다.
"""
import sys
import os

# 모듈화된 파일들에서 모든 기능 import
from config import (
    Config,
    get_unity_projects_from_directory,
    project_dirs,
    git_packages,
    GIT_BASE_URL,
    DEFAULT_BRANCH,
    DEV_BRANCH,
    COMMIT_MESSAGES,
    UNITY_EDITOR_PATH,
    UNITY_TIMEOUT,
    BUILD_TIMEOUT,
    BUILD_OUTPUT_DIR,
    WEBGL_CODE_OPTIMIZATION
)

from git_utils import (
    GitUtils,
    run_git_command,
    get_project_name_from_path,
    get_repository_url,
    is_git_repository,
    initialize_git_repository,
    get_current_branch,
    get_all_branches,
    get_branch_hierarchy_info,
    find_deepest_branch,
    branch_exists,
    create_and_checkout_branch,
    checkout_branch,
    get_target_branch,
    check_git_status,
    clean_untracked_files,
    reset_git_index,
    commit_changes,
    push_changes,
    commit_and_push_changes
)

from unity_cli import (
    find_unity_editor_path,
    run_unity_batch_mode,
    process_unity_project_batch,
    create_unity_batch_script,
    process_multiple_projects_parallel
)

from system_manager import (
    SYSTEM_MANAGER_METHODS,
    find_system_manager_files,
    has_method,
    add_method_to_script,
    add_methods_to_system_managers,
    add_custom_method_to_system_managers,
    add_hello_world_method_to_system_manager,
    add_hello_world_call_to_start_method,
    add_hello_world_to_all_system_managers
)

from package_manager import (
    add_git_packages_to_manifest
)

from build_manager import (
    create_unity_webgl_build_script,
    run_unity_webgl_build,
    build_multiple_webgl_projects,
    build_multiple_webgl_projects_sequential,
    build_multiple_webgl_projects_parallel,
    clean_build_outputs,
    format_bytes
)

from main import (
    print_usage,
    main
)

# 호환성을 위한 전역 변수 재선언 (원본 파일과 동일한 구조 유지)
# 이미 config.py에서 import했지만, 명시적으로 재선언하여 호환성 보장

# 모든 기능을 모듈화된 파일들에서 import했으므로,
# 원본 파일의 모든 함수와 클래스가 동일한 이름으로 사용 가능합니다.

if __name__ == "__main__":
    # 메인 실행부는 main.py에서 import
    main()
