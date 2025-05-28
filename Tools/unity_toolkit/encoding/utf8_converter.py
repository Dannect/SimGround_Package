"""
UTF-8 인코딩 변환 모듈

C# 스크립트 파일들을 UTF-8 인코딩으로 변환하는 기능을 제공합니다.
"""

import os
import chardet
from typing import List, Dict, Tuple
from ..config.settings import UTF8_TARGET_EXTENSIONS, EXCLUDED_DIRECTORIES


class UTF8Converter:
    """UTF-8 인코딩 변환 클래스"""
    
    def __init__(self):
        """UTF8Converter 초기화"""
        self.m_ConvertedFiles = []
        self.m_SkippedFiles = []
        self.m_ErrorFiles = []
    
    def convert_file_to_utf8(self, file_path: str) -> bool:
        """
        단일 파일을 UTF-8로 변환합니다.
        
        Args:
            file_path: 변환할 파일 경로
            
        Returns:
            변환 성공 여부
        """
        try:
            # 파일의 원래 인코딩 감지
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
            
            # 이미 UTF-8이면 변환하지 않음
            if encoding and encoding.lower().replace('-', '') == 'utf8':
                self.m_SkippedFiles.append(file_path)
                return False  # 변환하지 않음
            
            # 감지된 인코딩으로 읽어서 UTF-8로 저장
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.m_ConvertedFiles.append(file_path)
            return True  # 변환함
            
        except Exception as e:
            print(f"  ❌ {os.path.basename(file_path)} 변환 실패: {e}")
            self.m_ErrorFiles.append((file_path, str(e)))
            return False
    
    def convert_project_files(self, project_path: str) -> Dict[str, any]:
        """
        프로젝트의 모든 대상 파일을 UTF-8로 변환합니다.
        
        Args:
            project_path: Unity 프로젝트 경로
            
        Returns:
            변환 결과 딕셔너리
        """
        print(f"📝 UTF-8 변환 시작: {os.path.basename(project_path)}")
        
        # 결과 초기화
        self.m_ConvertedFiles.clear()
        self.m_SkippedFiles.clear()
        self.m_ErrorFiles.clear()
        
        assets_dir = os.path.join(project_path, "Assets")
        if not os.path.exists(assets_dir):
            print(f"  ❌ Assets 폴더 없음: {project_path}")
            return {
                'success': False,
                'converted_count': 0,
                'skipped_count': 0,
                'error_count': 0,
                'message': 'Assets 폴더 없음'
            }
        
        # Assets 폴더의 모든 대상 파일 처리
        for root, dirs, files in os.walk(assets_dir):
            # 제외할 디렉토리 필터링
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDED_DIRECTORIES]
            
            for file in files:
                # 대상 확장자 확인
                if any(file.endswith(ext) for ext in UTF8_TARGET_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    
                    try:
                        converted = self.convert_file_to_utf8(file_path)
                        if converted:
                            print(f"  ✅ {file} 변환 완료")
                        else:
                            print(f"  ⚪ {file} 이미 UTF-8, 변환 생략")
                    except Exception as e:
                        print(f"  ❌ {file} 변환 실패: {e}")
        
        # 결과 요약
        converted_count = len(self.m_ConvertedFiles)
        skipped_count = len(self.m_SkippedFiles)
        error_count = len(self.m_ErrorFiles)
        total_count = converted_count + skipped_count + error_count
        
        print(f"  📊 변환 결과: {converted_count}개 변환, {skipped_count}개 생략, {error_count}개 오류")
        
        return {
            'success': error_count == 0,
            'converted_count': converted_count,
            'skipped_count': skipped_count,
            'error_count': error_count,
            'total_count': total_count,
            'converted_files': self.m_ConvertedFiles.copy(),
            'skipped_files': self.m_SkippedFiles.copy(),
            'error_files': self.m_ErrorFiles.copy(),
            'message': f'{converted_count}개 파일 UTF-8 변환 완료'
        }
    
    def convert_multiple_projects(self, project_paths: List[str]) -> Dict[str, Dict[str, any]]:
        """
        여러 프로젝트의 파일들을 UTF-8로 변환합니다.
        
        Args:
            project_paths: Unity 프로젝트 경로 리스트
            
        Returns:
            프로젝트별 변환 결과 딕셔너리
        """
        results = {}
        
        for project_path in project_paths:
            if not os.path.exists(project_path):
                print(f"❌ 프로젝트 경로가 존재하지 않습니다: {project_path}")
                continue
            
            project_name = os.path.basename(project_path)
            results[project_name] = self.convert_project_files(project_path)
        
        return results
    
    def get_conversion_summary(self, results: Dict[str, Dict[str, any]]) -> Dict[str, int]:
        """
        변환 결과 요약을 생성합니다.
        
        Args:
            results: convert_multiple_projects의 결과
            
        Returns:
            전체 요약 딕셔너리
        """
        summary = {
            'total_projects': len(results),
            'successful_projects': 0,
            'total_converted': 0,
            'total_skipped': 0,
            'total_errors': 0
        }
        
        for project_name, result in results.items():
            if result['success']:
                summary['successful_projects'] += 1
            
            summary['total_converted'] += result['converted_count']
            summary['total_skipped'] += result['skipped_count']
            summary['total_errors'] += result['error_count']
        
        return summary
    
    def print_conversion_report(self, results: Dict[str, Dict[str, any]]):
        """변환 결과 보고서를 출력합니다."""
        summary = self.get_conversion_summary(results)
        
        print(f"\n=== UTF-8 변환 결과 보고서 ===")
        print(f"처리된 프로젝트: {summary['total_projects']}개")
        print(f"성공한 프로젝트: {summary['successful_projects']}개")
        print(f"총 변환된 파일: {summary['total_converted']}개")
        print(f"총 생략된 파일: {summary['total_skipped']}개")
        print(f"총 오류 파일: {summary['total_errors']}개")
        
        if summary['total_errors'] > 0:
            print(f"\n❌ 오류가 발생한 프로젝트:")
            for project_name, result in results.items():
                if result['error_count'] > 0:
                    print(f"  - {project_name}: {result['error_count']}개 오류")
        
        print("=" * 40)
    
    def detect_file_encoding(self, file_path: str) -> Tuple[str, float]:
        """
        파일의 인코딩을 감지합니다.
        
        Args:
            file_path: 파일 경로
            
        Returns:
            (인코딩, 신뢰도) 튜플
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return result['encoding'], result['confidence']
        except Exception:
            return 'unknown', 0.0
    
    def scan_project_encodings(self, project_path: str) -> Dict[str, List[str]]:
        """
        프로젝트의 파일 인코딩 현황을 스캔합니다.
        
        Args:
            project_path: Unity 프로젝트 경로
            
        Returns:
            인코딩별 파일 목록 딕셔너리
        """
        encoding_groups = {}
        
        assets_dir = os.path.join(project_path, "Assets")
        if not os.path.exists(assets_dir):
            return encoding_groups
        
        for root, dirs, files in os.walk(assets_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDED_DIRECTORIES]
            
            for file in files:
                if any(file.endswith(ext) for ext in UTF8_TARGET_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    encoding, confidence = self.detect_file_encoding(file_path)
                    
                    if encoding:
                        if encoding not in encoding_groups:
                            encoding_groups[encoding] = []
                        encoding_groups[encoding].append(file_path)
        
        return encoding_groups
    
    def print_encoding_report(self, project_path: str):
        """프로젝트의 인코딩 현황 보고서를 출력합니다."""
        project_name = os.path.basename(project_path)
        encoding_groups = self.scan_project_encodings(project_path)
        
        print(f"\n=== {project_name} 인코딩 현황 ===")
        
        if not encoding_groups:
            print("대상 파일이 없습니다.")
            return
        
        total_files = sum(len(files) for files in encoding_groups.values())
        
        for encoding, files in encoding_groups.items():
            percentage = (len(files) / total_files) * 100
            print(f"{encoding}: {len(files)}개 파일 ({percentage:.1f}%)")
            
            # UTF-8이 아닌 파일들 표시
            if encoding.lower().replace('-', '') != 'utf8':
                for file_path in files[:5]:  # 처음 5개만 표시
                    relative_path = os.path.relpath(file_path, project_path)
                    print(f"  - {relative_path}")
                if len(files) > 5:
                    print(f"  ... 외 {len(files) - 5}개")
        
        print(f"총 {total_files}개 파일")
        print("=" * 40) 