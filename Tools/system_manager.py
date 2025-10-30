"""
SystemManager 메소드 추가 함수들
"""
import os
import re
from git_utils import get_project_name_from_path

# SystemManager에 추가할 메소드 템플릿들
SYSTEM_MANAGER_METHODS = {
    "AllowKeyboardInput": '''    public void AllowKeyboardInput(bool isAllow)
    {
        Debug.Log("AllowKeyboardInput!" + isAllow);
#if UNITY_WEBGL && !UNITY_EDITOR
        WebGLInput.captureAllKeyboardInput = isAllow;
#endif
    }''',
    
    # 다른 메소드들도 여기에 추가 가능
    # "OtherMethod": '''    public void OtherMethod()
    # {
    #     // 메소드 내용
    # }''',
}

def find_system_manager_files(project_dirs):
    """모든 프로젝트에서 SystemManager.cs 파일들을 찾습니다."""
    system_manager_files = []
    
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            continue
            
        assets_dir = os.path.join(project_dir, "Assets")
        if not os.path.exists(assets_dir):
            continue
        
        project_name = get_project_name_from_path(project_dir)
        
        # Assets 폴더에서 SystemManager.cs 파일 찾기
        for root, dirs, files in os.walk(assets_dir):
            # Library, Temp 등 불필요한 폴더 제외
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Library', 'Temp', 'Logs']]
            
            for file in files:
                if file == "SystemManager.cs":
                    filepath = os.path.join(root, file)
                    system_manager_files.append((project_name, filepath))
                    print(f"SystemManager 발견: {project_name} - {os.path.relpath(filepath, project_dir)}")
    
    return system_manager_files

def has_method(filepath, method_name):
    """스크립트에 특정 메소드가 이미 존재하는지 확인합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 메소드 시그니처 패턴들 (다양한 접근 제한자와 형태 고려)
        patterns = [
            rf'(public|private|protected|internal)?\s*(static)?\s*(void|bool|int|float|string|[A-Z]\w*)\s+{method_name}\s*\(',
            rf'{method_name}\s*\(',  # 단순 패턴도 확인
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
        
    except Exception as e:
        print(f"메소드 존재 확인 실패 ({filepath}): {e}")
        return True  # 오류 시 안전하게 이미 존재한다고 가정

def add_method_to_script(filepath, method_name, method_content):
    """스크립트의 클래스 끝에 메소드를 추가합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 클래스의 마지막 닫는 중괄호 찾기 (더 안전한 방식)
        lines = content.split('\n')
        
        # 클래스 선언 찾기
        class_start_line = -1
        for i, line in enumerate(lines):
            if ('class ' in line and 'SystemManager' in line) or ('public class' in line):
                class_start_line = i
                break
        
        if class_start_line == -1:
            print(f"클래스 선언을 찾을 수 없습니다: {filepath}")
            return False
        
        # 클래스 시작 이후에서 마지막 중괄호 찾기
        last_brace_index = -1
        brace_count = 0
        in_class = False
        
        for i in range(class_start_line, len(lines)):
            line = lines[i].strip()
            
            # 클래스 시작 중괄호 찾기
            if not in_class and '{' in line:
                in_class = True
                brace_count = 1
                continue
            
            if in_class:
                # 중괄호 계산
                brace_count += line.count('{')
                brace_count -= line.count('}')
                
                # 클래스가 끝나는 지점 (brace_count가 0이 되는 지점)
                if brace_count == 0:
                    last_brace_index = i
                    break
        
        if last_brace_index == -1:
            print(f"클래스 닫는 중괄호를 찾을 수 없습니다: {filepath}")
            return False
        
        # 메소드 추가 (닫는 중괄호 바로 전에)
        lines.insert(last_brace_index, "")  # 빈 줄 추가
        lines.insert(last_brace_index + 1, method_content)
        
        # 파일에 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return True
        
    except Exception as e:
        print(f"메소드 추가 실패 ({filepath}): {e}")
        return False

def add_methods_to_system_managers(project_dirs, method_names=None):
    """모든 SystemManager에 지정된 메소드들을 추가합니다."""
    if method_names is None:
        method_names = ["AllowKeyboardInput"]  # 기본값
    
    print(f"\n=== SystemManager 메소드 추가 시작 ===")
    print(f"추가할 메소드: {', '.join(method_names)}")
    
    # SystemManager 파일들 찾기
    system_manager_files = find_system_manager_files(project_dirs)
    
    if not system_manager_files:
        print("SystemManager.cs 파일을 찾을 수 없습니다.")
        return False
    
    print(f"총 {len(system_manager_files)}개 SystemManager 파일 발견")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for project_name, filepath in system_manager_files:
        print(f"\n--- {project_name} SystemManager 처리 ---")
        
        methods_added = []
        methods_skipped = []
        
        for method_name in method_names:
            if method_name not in SYSTEM_MANAGER_METHODS:
                print(f"  ❌ 알 수 없는 메소드: {method_name}")
                continue
            
            # 메소드가 이미 존재하는지 확인
            if has_method(filepath, method_name):
                print(f"  ⚪ {method_name}: 이미 존재함, 생략")
                methods_skipped.append(method_name)
                continue
            
            # 메소드 추가
            method_content = SYSTEM_MANAGER_METHODS[method_name]
            if add_method_to_script(filepath, method_name, method_content):
                print(f"  ✅ {method_name}: 추가 완료")
                methods_added.append(method_name)
            else:
                print(f"  ❌ {method_name}: 추가 실패")
        
        # 결과 집계
        if methods_added:
            success_count += 1
            print(f"  📊 {project_name}: {len(methods_added)}개 메소드 추가됨")
        elif methods_skipped:
            skip_count += 1
            print(f"  📊 {project_name}: 모든 메소드가 이미 존재함")
        else:
            fail_count += 1
            print(f"  📊 {project_name}: 메소드 추가 실패")
    
    print(f"\n=== SystemManager 메소드 추가 결과 ===")
    print(f"성공 (메소드 추가됨): {success_count}개")
    print(f"생략 (이미 존재): {skip_count}개") 
    print(f"실패: {fail_count}개")
    print(f"총 처리: {len(system_manager_files)}개")
    
    return success_count > 0

def add_custom_method_to_system_managers(project_dirs, method_name, method_content):
    """사용자 정의 메소드를 SystemManager에 추가합니다."""
    print(f"\n=== 사용자 정의 메소드 추가: {method_name} ===")
    
    # 임시로 메소드 템플릿에 추가
    original_methods = SYSTEM_MANAGER_METHODS.copy()
    SYSTEM_MANAGER_METHODS[method_name] = method_content
    
    try:
        result = add_methods_to_system_managers(project_dirs, [method_name])
        return result
    finally:
        # 원래 템플릿으로 복원
        SYSTEM_MANAGER_METHODS.clear()
        SYSTEM_MANAGER_METHODS.update(original_methods)

def add_hello_world_method_to_system_manager(filepath):
    """SystemManager에 Hello World 메소드를 추가합니다."""
    hello_world_method = '''    private void PrintHelloWorld()
    {
        Debug.Log("Hello World!");
    }'''
    
    # 메소드가 이미 존재하는지 확인
    if has_method(filepath, "PrintHelloWorld"):
        print(f"  ⚪ PrintHelloWorld 메소드가 이미 존재합니다.")
        return True
    
    # 메소드 추가
    if add_method_to_script(filepath, "PrintHelloWorld", hello_world_method):
        print(f"  ✅ PrintHelloWorld 메소드 추가 완료")
        return True
    else:
        print(f"  ❌ PrintHelloWorld 메소드 추가 실패")
        return False

def add_hello_world_call_to_start_method(filepath):
    """SystemManager의 Start() 함수 가장 아래에 PrintHelloWorld() 호출을 추가합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Start() 메소드를 찾아서 그 끝에 PrintHelloWorld() 호출 추가
        lines = content.split('\n')
        
        # Start() 메소드 찾기 (더 정확한 패턴)
        start_method_found = False
        start_method_line = -1
        method_brace_count = 0
        start_method_end_line = -1
        start_brace_found = False
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Start() 메소드 시작 찾기 (더 정확한 패턴)
            if not start_method_found and ('void Start()' in line or 'void Start(' in line) and ('private' in line or 'public' in line or 'protected' in line or stripped_line.startswith('void')):
                start_method_found = True
                start_method_line = i
                print(f"  📍 Start() 메소드 발견: {start_method_line + 1}번째 줄")
                
                # 같은 줄에 중괄호가 있는지 확인
                if '{' in line:
                    start_brace_found = True
                    method_brace_count = 1
                continue
            
            # Start() 메소드 내부에서 중괄호 카운팅
            if start_method_found and start_method_end_line == -1:
                # 시작 중괄호를 아직 못 찾았다면 찾기
                if not start_brace_found and '{' in stripped_line:
                    start_brace_found = True
                    method_brace_count = 1
                    continue
                
                # 시작 중괄호를 찾았다면 중괄호 카운팅 시작
                if start_brace_found:
                    method_brace_count += stripped_line.count('{')
                    method_brace_count -= stripped_line.count('}')
                    
                    # Start() 메소드가 끝나는 지점
                    if method_brace_count == 0:
                        start_method_end_line = i
                        print(f"  📍 Start() 메소드 끝: {start_method_end_line + 1}번째 줄")
                        break
        
        if not start_method_found:
            print(f"  ❌ Start() 메소드를 찾을 수 없습니다.")
            return False
        
        if start_method_end_line == -1:
            print(f"  ❌ Start() 메소드의 끝을 찾을 수 없습니다.")
            return False
        
        # 이미 PrintHelloWorld() 호출이 있는지 확인
        start_method_content = '\n'.join(lines[start_method_line:start_method_end_line + 1])
        if 'PrintHelloWorld()' in start_method_content:
            print(f"  ⚪ Start() 메소드에 PrintHelloWorld() 호출이 이미 존재합니다.")
            return True
        
        # Start() 메소드 끝 바로 전에 PrintHelloWorld() 호출 추가
        # 닫는 중괄호 바로 전에 들여쓰기와 함께 추가
        indent = "        "  # 8칸 들여쓰기 (일반적인 메소드 내부 들여쓰기)
        
        # 기존 줄의 들여쓰기 패턴 분석 (Start() 메소드 내부에서)
        for check_line in range(start_method_end_line - 1, start_method_line, -1):
            if lines[check_line].strip() and not lines[check_line].strip().startswith('}'):
                # 비어있지 않고 닫는 중괄호가 아닌 줄의 들여쓰기 패턴을 가져옴
                leading_spaces = len(lines[check_line]) - len(lines[check_line].lstrip())
                if leading_spaces > 0:
                    indent = ' ' * leading_spaces
                    break
        
        lines.insert(start_method_end_line, f"{indent}PrintHelloWorld();")
        lines.insert(start_method_end_line, "")  # 빈 줄 추가
        
        # 파일에 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  ✅ Start() 메소드에 PrintHelloWorld() 호출 추가 완료")
        return True
        
    except Exception as e:
        print(f"  ❌ Start() 메소드 수정 실패: {e}")
        return False

def add_hello_world_to_all_system_managers(project_dirs):
    """모든 SystemManager에 Hello World 메소드를 추가하고 Start() 함수에서 호출하도록 설정합니다."""
    print(f"\n=== SystemManager Hello World 메소드 추가 시작 ===")
    
    # SystemManager 파일들 찾기
    system_manager_files = find_system_manager_files(project_dirs)
    
    if not system_manager_files:
        print("SystemManager.cs 파일을 찾을 수 없습니다.")
        return False
    
    print(f"총 {len(system_manager_files)}개 SystemManager 파일 발견")
    
    success_count = 0
    fail_count = 0
    
    for project_name, filepath in system_manager_files:
        print(f"\n--- {project_name} SystemManager 처리 ---")
        
        # 1. Hello World 메소드 추가
        method_added = add_hello_world_method_to_system_manager(filepath)
        
        # 2. Start() 함수에 호출 추가
        call_added = add_hello_world_call_to_start_method(filepath)
        
        # 결과 집계
        if method_added and call_added:
            success_count += 1
            print(f"  📊 {project_name}: Hello World 메소드 추가 및 Start() 호출 설정 완료")
        else:
            fail_count += 1
            print(f"  📊 {project_name}: Hello World 설정 실패")
    
    print(f"\n=== SystemManager Hello World 메소드 추가 결과 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")
    print(f"총 처리: {len(system_manager_files)}개")
    
    return success_count > 0

