"""
Unity 툴킷 메인 클래스

모든 Unity 개발 자동화 기능을 통합하여 제공하는 메인 클래스입니다.
각 모듈의 기능을 조합하여 복합적인 작업을 수행할 수 있습니다.
"""

import os
from typing import List, Dict, Tuple, Optional
from .core.project_manager import ProjectManager
from .encoding.utf8_converter import UTF8Converter
from .git.repository_manager import GitRepositoryManager
from .unity.package_manager import UnityPackageManager
from .unity.build_manager import UnityBuildManager
from .unity.api_compatibility import Unity6APIFixer


class UnityToolkit:
    """
    Unity 개발 자동화를 위한 통합 툴킷 클래스
    
    이 클래스는 Unity 프로젝트 개발에 필요한 모든 자동화 기능을 
    하나의 인터페이스로 제공합니다.
    """
    
    def __init__(self, project_paths: List[str] = None):
        """
        UnityToolkit 초기화
        
        Args:
            project_paths: Unity 프로젝트 경로 리스트
        """
        self.project_manager = ProjectManager(project_paths or [])
        self.utf8_converter = UTF8Converter()
        self.git_manager = GitRepositoryManager()
        self.package_manager = UnityPackageManager()
        self.build_manager = UnityBuildManager()
        self.api_fixer = Unity6APIFixer()
        
        # 작업 결과 저장
        self.last_results = {}
    
    def add_project(self, project_path: str) -> bool:
        """프로젝트를 추가합니다."""
        return self.project_manager.add_project(project_path)
    
    def remove_project(self, project_path: str) -> bool:
        """프로젝트를 제거합니다."""
        return self.project_manager.remove_project(project_path)
    
    def get_projects(self) -> List[str]:
        """등록된 프로젝트 목록을 반환합니다."""
        return self.project_manager.get_projects()
    
    # =========================
    # #region 통합 워크플로우 메서드들
    # =========================
    
    def full_automation_workflow(self, 
                                commit_message: str = "Auto commit: Unity project updates",
                                include_unity_batch: bool = False,
                                parallel_processing: bool = False) -> Dict[str, any]:
        """
        전체 자동화 워크플로우를 실행합니다.
        
        실행 순서:
        1. UTF-8 인코딩 변환
        2. Unity 6 API 호환성 수정
        3. Unity 패키지 추가
        4. Git 커밋 및 푸시
        5. Unity 배치 모드 실행 (선택사항)
        
        Args:
            commit_message: Git 커밋 메시지
            include_unity_batch: Unity 배치 모드 실행 여부
            parallel_processing: 병렬 처리 여부
            
        Returns:
            각 단계별 실행 결과를 담은 딕셔너리
        """
        print("=== Unity 프로젝트 전체 자동화 워크플로우 시작 ===\n")
        
        results = {
            'utf8_conversion': {},
            'unity6_fixes': {},
            'package_updates': {},
            'git_operations': {},
            'unity_batch': {} if include_unity_batch else None
        }
        
        projects = self.project_manager.get_projects()
        
        # 1. UTF-8 인코딩 변환
        print("1. UTF-8 인코딩 변환 시작...")
        for project_path in projects:
            project_name = os.path.basename(project_path)
            print(f"  - {project_name} 처리 중...")
            result = self.utf8_converter.convert_project_files(project_path)
            results['utf8_conversion'][project_name] = result
        
        # 2. Unity 6 API 호환성 수정
        print("\n2. Unity 6 API 호환성 수정 시작...")
        for project_path in projects:
            project_name = os.path.basename(project_path)
            print(f"  - {project_name} 처리 중...")
            result = self.api_fixer.fix_project_apis(project_path)
            results['unity6_fixes'][project_name] = result
        
        # 3. Unity 패키지 추가
        print("\n3. Unity 패키지 업데이트 시작...")
        for project_path in projects:
            project_name = os.path.basename(project_path)
            print(f"  - {project_name} 처리 중...")
            result = self.package_manager.update_project_packages(project_path)
            results['package_updates'][project_name] = result
        
        # 4. Git 커밋 및 푸시
        print("\n4. Git 커밋 및 푸시 시작...")
        for project_path in projects:
            project_name = os.path.basename(project_path)
            print(f"  - {project_name} 처리 중...")
            result = self.git_manager.commit_and_push_changes(project_path, commit_message)
            results['git_operations'][project_name] = result
        
        # 5. Unity 배치 모드 실행 (선택사항)
        if include_unity_batch:
            print("\n5. Unity 배치 모드 실행 시작...")
            if parallel_processing:
                batch_results = self.run_unity_batch_parallel(projects)
            else:
                batch_results = self.run_unity_batch_sequential(projects)
            results['unity_batch'] = batch_results
        
        # 결과 저장
        self.last_results = results
        
        print("\n=== 전체 자동화 워크플로우 완료 ===")
        self._print_workflow_summary(results)
        
        return results
    
    def build_automation_workflow(self, 
                                 build_target: str = "WebGL",
                                 parallel_build: bool = False,
                                 clean_before_build: bool = True) -> Dict[str, any]:
        """
        빌드 자동화 워크플로우를 실행합니다.
        
        Args:
            build_target: 빌드 타겟 (WebGL, Windows, etc.)
            parallel_build: 병렬 빌드 여부
            clean_before_build: 빌드 전 정리 여부
            
        Returns:
            빌드 결과를 담은 딕셔너리
        """
        print(f"=== Unity {build_target} 빌드 자동화 워크플로우 시작 ===\n")
        
        projects = self.project_manager.get_projects()
        
        # 빌드 전 정리
        if clean_before_build:
            print("빌드 출력물 정리 중...")
            self.build_manager.clean_build_outputs(projects)
        
        # 빌드 실행
        if build_target.upper() == "WEBGL":
            results = self.build_manager.build_multiple_webgl_projects(
                projects, 
                parallel=parallel_build
            )
        else:
            print(f"지원하지 않는 빌드 타겟: {build_target}")
            return {}
        
        print(f"\n=== {build_target} 빌드 자동화 워크플로우 완료 ===")
        return results
    
    def maintenance_workflow(self) -> Dict[str, any]:
        """
        프로젝트 유지보수 워크플로우를 실행합니다.
        
        실행 내용:
        - Unity 6 호환성 검사
        - 프로젝트 상태 검증
        - Git 상태 확인
        
        Returns:
            유지보수 결과를 담은 딕셔너리
        """
        print("=== Unity 프로젝트 유지보수 워크플로우 시작 ===\n")
        
        results = {
            'project_validation': {},
            'unity6_compatibility': {},
            'git_status': {}
        }
        
        projects = self.project_manager.get_projects()
        
        # 프로젝트 검증
        print("1. 프로젝트 상태 검증...")
        for project_path in projects:
            project_name = os.path.basename(project_path)
            is_valid = self.project_manager.validate_unity_project(project_path)
            results['project_validation'][project_name] = is_valid
            print(f"  - {project_name}: {'✅ 유효' if is_valid else '❌ 무효'}")
        
        # Unity 6 호환성 검사
        print("\n2. Unity 6 호환성 검사...")
        compatibility_report = self.api_fixer.create_compatibility_report(projects)
        results['unity6_compatibility'] = compatibility_report
        
        # Git 상태 확인
        print("\n3. Git 상태 확인...")
        for project_path in projects:
            project_name = os.path.basename(project_path)
            git_status = self.git_manager.check_git_status(project_path)
            results['git_status'][project_name] = git_status
            print(f"  - {project_name}: {git_status}")
        
        print("\n=== 유지보수 워크플로우 완료 ===")
        return results
    
    # =========================
    # #region 개별 기능 메서드들
    # =========================
    
    def convert_all_to_utf8(self) -> Dict[str, any]:
        """모든 프로젝트의 C# 파일을 UTF-8로 변환합니다."""
        results = {}
        for project_path in self.project_manager.get_projects():
            project_name = os.path.basename(project_path)
            results[project_name] = self.utf8_converter.convert_project_files(project_path)
        return results
    
    def fix_all_unity6_apis(self) -> Dict[str, any]:
        """모든 프로젝트의 Unity 6 API 호환성을 수정합니다."""
        results = {}
        for project_path in self.project_manager.get_projects():
            project_name = os.path.basename(project_path)
            results[project_name] = self.api_fixer.fix_project_apis(project_path)
        return results
    
    def update_all_packages(self, packages: Dict[str, str] = None) -> Dict[str, any]:
        """모든 프로젝트의 Unity 패키지를 업데이트합니다."""
        results = {}
        for project_path in self.project_manager.get_projects():
            project_name = os.path.basename(project_path)
            if packages:
                results[project_name] = self.package_manager.add_packages_to_project(project_path, packages)
            else:
                results[project_name] = self.package_manager.update_project_packages(project_path)
        return results
    
    def commit_all_changes(self, commit_message: str = "Auto commit: Unity project updates") -> Dict[str, any]:
        """모든 프로젝트의 변경사항을 커밋하고 푸시합니다."""
        results = {}
        for project_path in self.project_manager.get_projects():
            project_name = os.path.basename(project_path)
            results[project_name] = self.git_manager.commit_and_push_changes(project_path, commit_message)
        return results
    
    def run_unity_batch_sequential(self, projects: List[str] = None) -> Dict[str, any]:
        """Unity 배치 모드를 순차적으로 실행합니다."""
        if projects is None:
            projects = self.project_manager.get_projects()
        
        results = {}
        for project_path in projects:
            project_name = os.path.basename(project_path)
            results[project_name] = self.build_manager.process_unity_project_batch(project_path)
        return results
    
    def run_unity_batch_parallel(self, projects: List[str] = None, max_workers: int = 3) -> Dict[str, any]:
        """Unity 배치 모드를 병렬로 실행합니다."""
        if projects is None:
            projects = self.project_manager.get_projects()
        
        return self.build_manager.process_multiple_projects_parallel(projects, max_workers)
    
    # =========================
    # #region 유틸리티 메서드들
    # =========================
    
    def get_last_results(self) -> Dict[str, any]:
        """마지막 실행 결과를 반환합니다."""
        return self.last_results
    
    def print_project_summary(self):
        """등록된 프로젝트들의 요약 정보를 출력합니다."""
        projects = self.project_manager.get_projects()
        print(f"\n=== 등록된 Unity 프로젝트 ({len(projects)}개) ===")
        
        for i, project_path in enumerate(projects, 1):
            project_name = os.path.basename(project_path)
            is_valid = self.project_manager.validate_unity_project(project_path)
            is_git = self.git_manager.is_git_repository(project_path)
            
            print(f"{i:2d}. {project_name}")
            print(f"    경로: {project_path}")
            print(f"    상태: {'✅ 유효' if is_valid else '❌ 무효'}")
            print(f"    Git: {'✅ 초기화됨' if is_git else '❌ 미초기화'}")
            print()
    
    def _print_workflow_summary(self, results: Dict[str, any]):
        """워크플로우 실행 결과 요약을 출력합니다."""
        print("\n=== 워크플로우 실행 결과 요약 ===")
        
        for step_name, step_results in results.items():
            if step_results is None:
                continue
                
            print(f"\n📋 {step_name.replace('_', ' ').title()}:")
            
            if isinstance(step_results, dict):
                success_count = sum(1 for result in step_results.values() if result)
                total_count = len(step_results)
                print(f"  성공: {success_count}/{total_count}")
                
                # 실패한 프로젝트 표시
                failed_projects = [name for name, result in step_results.items() if not result]
                if failed_projects:
                    print(f"  실패: {', '.join(failed_projects)}")
            else:
                print(f"  결과: {step_results}")
        
        print("\n" + "="*50) 