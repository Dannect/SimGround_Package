"""
Unity CLI 자동화 함수들
"""
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import Config
from git_utils import get_project_name_from_path

# 전역 변수 참조 (호환성 유지)
UNITY_EDITOR_PATH = Config.UNITY_EDITOR_PATH
UNITY_TIMEOUT = Config.UNITY_TIMEOUT


def find_unity_editor_path():
    """Unity Editor 경로를 자동으로 찾습니다."""
    # 일반적인 Unity 설치 경로들
    common_paths = [
        r"C:\Program Files\Unity\Hub\Editor",
        r"C:\Program Files\Unity\Editor",
        r"C:\Program Files (x86)\Unity\Hub\Editor",
        r"C:\Program Files (x86)\Unity\Editor"
    ]
    
    for base_path in common_paths:
        if os.path.exists(base_path):
            # 버전 폴더들을 찾아서 가장 최신 버전 선택
            try:
                versions = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                if versions:
                    # 버전 정렬 (최신 버전 우선)
                    versions.sort(reverse=True)
                    unity_exe = os.path.join(base_path, versions[0], "Editor", "Unity.exe")
                    if os.path.exists(unity_exe):
                        return unity_exe
            except:
                continue
    
    return None

def run_unity_batch_mode(project_path, method_name=None, timeout=UNITY_TIMEOUT):
    """Unity를 배치 모드로 실행하여 Editor 스크립트를 실행합니다."""
    unity_path = UNITY_EDITOR_PATH
    
    # Unity 경로가 존재하지 않으면 자동 검색
    if not os.path.exists(unity_path):
        print(f"Unity 경로를 찾을 수 없습니다: {unity_path}")
        print("Unity 경로 자동 검색 중...")
        unity_path = find_unity_editor_path()
        if not unity_path:
            print("Unity Editor를 찾을 수 없습니다. UNITY_EDITOR_PATH를 확인해주세요.")
            return False
        print(f"Unity 경로 발견: {unity_path}")
    
    project_name = get_project_name_from_path(project_path)
    print(f"Unity 배치 모드 실행 중: {project_name}")
    
    # Unity 명령어 구성
    cmd = [
        unity_path,
        "-batchmode",           # 배치 모드
        "-quit",               # 완료 후 종료
        "-projectPath", project_path,  # 프로젝트 경로
        "-logFile", "-",       # 로그를 콘솔에 출력
    ]
    
    # 특정 메서드 실행이 지정된 경우
    if method_name:
        cmd.extend(["-executeMethod", method_name])
    
    try:
        print(f"Unity 명령어: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        
        # Unity 로그 출력
        if result.stdout:
            print("=== Unity 출력 ===")
            print(result.stdout)
        
        if result.stderr:
            print("=== Unity 오류 ===")
            print(result.stderr)
        
        # Unity는 성공해도 exit code가 0이 아닐 수 있음
        if result.returncode == 0:
            print(f"Unity 배치 모드 완료: {project_name}")
            return True
        else:
            print(f"Unity 배치 모드 경고 (exit code: {result.returncode}): {project_name}")
            # 로그에서 실제 오류 확인
            if "error" in result.stdout.lower() or "exception" in result.stdout.lower():
                print("실제 오류 발견, 실패로 처리")
                return False
            else:
                print("경고이지만 정상 처리된 것으로 판단")
                return True
                
    except subprocess.TimeoutExpired:
        print(f"Unity 실행 타임아웃 ({timeout}초): {project_name}")
        return False
    except Exception as e:
        print(f"Unity 실행 오류: {e}")
        return False

def process_unity_project_batch(project_path):
    """Unity 프로젝트를 배치 모드로 처리합니다."""
    project_name = get_project_name_from_path(project_path)
    
    if not os.path.exists(project_path):
        print(f"프로젝트 폴더가 존재하지 않습니다: {project_path}")
        return False
    
    # Unity 프로젝트인지 확인
    project_settings = os.path.join(project_path, "ProjectSettings", "ProjectSettings.asset")
    if not os.path.exists(project_settings):
        print(f"Unity 프로젝트가 아닙니다: {project_path}")
        return False
    
    print(f"\n=== {project_name} Unity 배치 처리 시작 ===")
    
    # Unity 배치 모드 실행 (패키지 임포트 및 프로젝트 설정 검증)
    success = run_unity_batch_mode(project_path)
    
    if success:
        print(f"=== {project_name} Unity 배치 처리 완료 ===")
        return True
    else:
        print(f"=== {project_name} Unity 배치 처리 실패 ===")
        return False

def create_unity_batch_script(project_path):
    """Unity Editor에서 실행할 배치 스크립트를 생성합니다."""
    script_dir = os.path.join(project_path, "Assets", "Editor", "BatchScripts")
    os.makedirs(script_dir, exist_ok=True)
    
    script_path = os.path.join(script_dir, "AutoBatchProcessor.cs")
    
    script_content = '''using UnityEngine;
using UnityEditor;
using System.IO;

public class AutoBatchProcessor
{
    [MenuItem("Tools/Process Batch")]
    public static void ProcessBatch()
    {
        Debug.Log("=== 배치 처리 시작 ===");
        
        // 패키지 임포트 및 Asset Database 갱신
        AssetDatabase.Refresh();
        
        // 프로젝트 설정 검증
        ValidateProjectSettings();
        
        // 최종 Asset Database 갱신
        AssetDatabase.Refresh();
        AssetDatabase.SaveAssets();
        
        Debug.Log("=== 배치 처리 완료 ===");
    }
    
    private static void ValidateProjectSettings()
    {
        Debug.Log("프로젝트 설정 검증 중...");
        
        // 기본 프로젝트 설정 확인
        if (string.IsNullOrEmpty(PlayerSettings.productName))
        {
            Debug.LogWarning("제품명이 설정되지 않았습니다.");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.companyName))
        {
            Debug.LogWarning("회사명이 설정되지 않았습니다.");
        }
        
        Debug.Log("프로젝트 설정 검증 완료");
    }
}
'''
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"배치 스크립트 생성 완료: {script_path}")
        return True
    except Exception as e:
        print(f"배치 스크립트 생성 실패: {e}")
        return False

def process_multiple_projects_parallel(project_dirs, max_workers=3):
    """여러 Unity 프로젝트를 병렬로 처리합니다."""
    print(f"\n=== 병렬 처리 시작 (최대 {max_workers}개 동시 실행) ===")
    
    success_count = 0
    fail_count = 0
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 모든 프로젝트를 병렬로 제출
        future_to_project = {
            executor.submit(process_unity_project_batch, project_dir): project_dir 
            for project_dir in project_dirs if os.path.exists(project_dir)
        }
        
        # 완료된 작업들을 처리
        for future in as_completed(future_to_project):
            project_dir = future_to_project[future]
            project_name = get_project_name_from_path(project_dir)
            
            try:
                result = future.result()
                if result:
                    success_count += 1
                    print(f"✅ {project_name} 병렬 처리 완료")
                else:
                    fail_count += 1
                    print(f"❌ {project_name} 병렬 처리 실패")
                results.append((project_name, result))
            except Exception as e:
                fail_count += 1
                print(f"❌ {project_name} 병렬 처리 예외: {e}")
                results.append((project_name, False))
    
    print(f"\n=== 병렬 처리 결과 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 처리: {success_count + fail_count}개")
    
    return results

