"""
Unity 프로젝트 관리 모듈

Unity 프로젝트들의 관리, 검증, 추가/제거 등의 기능을 제공합니다.
"""

import os
from typing import List, Optional
from ..config.settings import DEFAULT_PROJECT_PATHS, validate_project_paths


class ProjectManager:
    """Unity 프로젝트 관리 클래스"""
    
    def __init__(self, project_paths: List[str] = None):
        """
        ProjectManager 초기화
        
        Args:
            project_paths: Unity 프로젝트 경로 리스트
        """
        self.m_ProjectPaths = project_paths or DEFAULT_PROJECT_PATHS.copy()
        self._validate_all_projects()
    
    def add_project(self, project_path: str) -> bool:
        """
        프로젝트를 추가합니다.
        
        Args:
            project_path: 추가할 Unity 프로젝트 경로
            
        Returns:
            추가 성공 여부
        """
        if not os.path.exists(project_path):
            print(f"❌ 프로젝트 경로가 존재하지 않습니다: {project_path}")
            return False
        
        if not self.validate_unity_project(project_path):
            print(f"❌ 유효한 Unity 프로젝트가 아닙니다: {project_path}")
            return False
        
        if project_path in self.m_ProjectPaths:
            print(f"⚠️ 이미 등록된 프로젝트입니다: {project_path}")
            return True
        
        self.m_ProjectPaths.append(project_path)
        print(f"✅ 프로젝트 추가 완료: {os.path.basename(project_path)}")
        return True
    
    def remove_project(self, project_path: str) -> bool:
        """
        프로젝트를 제거합니다.
        
        Args:
            project_path: 제거할 Unity 프로젝트 경로
            
        Returns:
            제거 성공 여부
        """
        if project_path not in self.m_ProjectPaths:
            print(f"⚠️ 등록되지 않은 프로젝트입니다: {project_path}")
            return False
        
        self.m_ProjectPaths.remove(project_path)
        print(f"✅ 프로젝트 제거 완료: {os.path.basename(project_path)}")
        return True
    
    def get_projects(self) -> List[str]:
        """
        등록된 프로젝트 목록을 반환합니다.
        
        Returns:
            Unity 프로젝트 경로 리스트
        """
        return self.m_ProjectPaths.copy()
    
    def get_valid_projects(self) -> List[str]:
        """
        유효한 프로젝트 목록만 반환합니다.
        
        Returns:
            유효한 Unity 프로젝트 경로 리스트
        """
        valid_projects = []
        for project_path in self.m_ProjectPaths:
            if self.validate_unity_project(project_path):
                valid_projects.append(project_path)
        return valid_projects
    
    def validate_unity_project(self, project_path: str) -> bool:
        """
        Unity 프로젝트 유효성을 검사합니다.
        
        Args:
            project_path: 검사할 프로젝트 경로
            
        Returns:
            유효한 Unity 프로젝트 여부
        """
        if not os.path.exists(project_path):
            return False
        
        # Unity 프로젝트 필수 폴더/파일 확인
        required_paths = [
            os.path.join(project_path, "Assets"),
            os.path.join(project_path, "ProjectSettings"),
            os.path.join(project_path, "ProjectSettings", "ProjectSettings.asset")
        ]
        
        for required_path in required_paths:
            if not os.path.exists(required_path):
                return False
        
        return True
    
    def get_project_info(self, project_path: str) -> dict:
        """
        프로젝트 정보를 반환합니다.
        
        Args:
            project_path: 프로젝트 경로
            
        Returns:
            프로젝트 정보 딕셔너리
        """
        info = {
            'name': os.path.basename(project_path),
            'path': project_path,
            'exists': os.path.exists(project_path),
            'is_valid': self.validate_unity_project(project_path),
            'has_assets': os.path.exists(os.path.join(project_path, "Assets")),
            'has_project_settings': os.path.exists(os.path.join(project_path, "ProjectSettings")),
            'has_packages': os.path.exists(os.path.join(project_path, "Packages")),
            'has_library': os.path.exists(os.path.join(project_path, "Library"))
        }
        
        # Unity 버전 정보 (ProjectVersion.txt에서 읽기)
        version_file = os.path.join(project_path, "ProjectSettings", "ProjectVersion.txt")
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('m_EditorVersion:'):
                            info['unity_version'] = line.split(':', 1)[1].strip()
                            break
            except Exception:
                info['unity_version'] = 'Unknown'
        else:
            info['unity_version'] = 'Unknown'
        
        return info
    
    def print_projects_summary(self):
        """등록된 프로젝트들의 요약 정보를 출력합니다."""
        projects = self.get_projects()
        print(f"\n=== Unity 프로젝트 관리자 ({len(projects)}개 프로젝트) ===")
        
        if not projects:
            print("등록된 프로젝트가 없습니다.")
            return
        
        valid_count = 0
        for i, project_path in enumerate(projects, 1):
            info = self.get_project_info(project_path)
            
            print(f"\n{i:2d}. {info['name']}")
            print(f"    경로: {info['path']}")
            print(f"    상태: {'✅ 유효' if info['is_valid'] else '❌ 무효'}")
            print(f"    Unity 버전: {info['unity_version']}")
            
            if info['is_valid']:
                valid_count += 1
            else:
                print(f"    문제: ", end="")
                issues = []
                if not info['exists']:
                    issues.append("경로 없음")
                if not info['has_assets']:
                    issues.append("Assets 폴더 없음")
                if not info['has_project_settings']:
                    issues.append("ProjectSettings 폴더 없음")
                print(", ".join(issues))
        
        print(f"\n📊 요약: 유효한 프로젝트 {valid_count}/{len(projects)}개")
        print("=" * 50)
    
    def _validate_all_projects(self):
        """모든 등록된 프로젝트의 유효성을 검사합니다."""
        invalid_projects = []
        
        for project_path in self.m_ProjectPaths:
            if not self.validate_unity_project(project_path):
                invalid_projects.append(project_path)
        
        if invalid_projects:
            print(f"⚠️ 유효하지 않은 프로젝트 {len(invalid_projects)}개 발견:")
            for project_path in invalid_projects:
                print(f"  - {project_path}")
    
    def cleanup_invalid_projects(self) -> int:
        """
        유효하지 않은 프로젝트들을 목록에서 제거합니다.
        
        Returns:
            제거된 프로젝트 수
        """
        invalid_projects = []
        
        for project_path in self.m_ProjectPaths:
            if not self.validate_unity_project(project_path):
                invalid_projects.append(project_path)
        
        for project_path in invalid_projects:
            self.m_ProjectPaths.remove(project_path)
            print(f"🗑️ 유효하지 않은 프로젝트 제거: {project_path}")
        
        return len(invalid_projects)
    
    def get_projects_by_unity_version(self, version_pattern: str = None) -> dict:
        """
        Unity 버전별로 프로젝트를 그룹화합니다.
        
        Args:
            version_pattern: 특정 버전 패턴 (예: "2022", "6000")
            
        Returns:
            버전별 프로젝트 딕셔너리
        """
        version_groups = {}
        
        for project_path in self.get_valid_projects():
            info = self.get_project_info(project_path)
            version = info['unity_version']
            
            if version_pattern and version_pattern not in version:
                continue
            
            if version not in version_groups:
                version_groups[version] = []
            
            version_groups[version].append(project_path)
        
        return version_groups 