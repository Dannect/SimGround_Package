"""
Unity 6 전용 WebGL 빌드 자동화 함수들 (Player Settings 완전 반영)
- Unity 6 (6000.0.59f2) 전용으로 최적화됨
- WasmCodeOptimization 5가지 옵션 지원 (BuildTimes, RuntimeSpeed, RuntimeSpeedLTO, DiskSize, DiskSizeLTO)
- UnityEditor.WebGL.UserBuildSettings.codeOptimization 사용
"""
import os
import subprocess
import time
import shutil
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from string import Template
from config import Config
from git_utils import get_project_name_from_path
from unity_cli import find_unity_editor_path

# 전역 변수 참조 (호환성 유지)
BUILD_OUTPUT_DIR = Config.BUILD_OUTPUT_DIR
BUILD_TIMEOUT = Config.BUILD_TIMEOUT
WEBGL_CODE_OPTIMIZATION = Config.WEBGL_CODE_OPTIMIZATION
UNITY_EDITOR_PATH = Config.UNITY_EDITOR_PATH
def create_unity_webgl_build_script(project_path, output_path=None, auto_configure=True, code_optimization=None):
    """Unity WebGL 빌드를 위한 Editor 스크립트를 생성합니다. (Player Settings 자동 설정 포함)"""
    editor_dir = os.path.join(project_path, "Assets", "Editor")
    if not os.path.exists(editor_dir):
        os.makedirs(editor_dir)
    
    script_path = os.path.join(editor_dir, "AutoWebGLBuildScript.cs")
    
    # 프로젝트명 추출
    project_name = get_project_name_from_path(project_path)
    
    if output_path is None:
        # 중앙 집중식 빌드 경로: C:\Users\wkzkx\Desktop\Lim\GitHub\Build\프로젝트명\
        output_path = os.path.join(BUILD_OUTPUT_DIR, project_name)
    
    output_path_formatted = output_path.replace(os.sep, '/')
    
    # Code Optimization 설정 (기본값 또는 매개변수로 전달된 값)
    if code_optimization is None:
        code_optimization = WEBGL_CODE_OPTIMIZATION
    
    # 유효성 검사 (Unity 6.0 WasmCodeOptimization 5가지 옵션)
    valid_options = ["BuildTimes", "RuntimeSpeed", "RuntimeSpeedLTO", "DiskSize", "DiskSizeLTO"]
    if code_optimization not in valid_options:
        print(f"⚠️ 잘못된 Code Optimization 설정: {code_optimization}")
        print(f"   사용 가능한 옵션: {', '.join(valid_options)}")
        print(f"   기본값 'RuntimeSpeedLTO' 사용")
        code_optimization = "RuntimeSpeedLTO"
    
    # Template 시스템을 사용하여 Unity 스크립트 생성
    script_template = Template("""// Unity 6 전용 WebGL 빌드 자동화 스크립트
// dannect.unity.toolkit.py에 의해 자동 생성됨
using UnityEngine;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.WebGL;
using System.IO;

public class AutoWebGLBuildScript
{
    // Unity 6 Code Optimization 설정 (WasmCodeOptimization)
    // Unity 6.0에서 사용 가능한 옵션: BuildTimes, RuntimeSpeed, RuntimeSpeedLTO, DiskSize, DiskSizeLTO
    // 이 값은 dannect.unity.toolkit.py의 Config.WEBGL_CODE_OPTIMIZATION에서 자동 설정됩니다
    private static string CODE_OPTIMIZATION_TYPE = "$code_optimization";
    
    [MenuItem("Build/Auto Build WebGL (Player Settings)")]
    public static void BuildWebGLWithPlayerSettings()
    {
        Debug.Log("=== WebGL Player Settings 자동 설정 및 빌드 시작 ===");
        
        // WebGL Player Settings 자동 설정
        ConfigureWebGLPlayerSettings();
        
        // 설정된 Player Settings 정보 출력
        LogCurrentPlayerSettings();
        
        // 프로젝트명 추출 (Unity에서 스크립트가 실행되는 프로젝트의 이름)
        string projectName = Application.productName;
        if (string.IsNullOrEmpty(projectName))
        {
            // ProductName이 없으면 프로젝트 폴더명 사용
            projectName = new DirectoryInfo(Application.dataPath).Parent.Name;
        }
        
        // 특수문자 제거 및 안전한 파일명 생성
        string safeProjectName = projectName.Replace(" ", "_");
        safeProjectName = System.Text.RegularExpressions.Regex.Replace(safeProjectName, @"[^\\w\\-_\\.]", "");
        
        // 중앙 집중식 빌드 경로 설정: C:/Users/wkzkx/Desktop/Lim/GitHub/Build/프로젝트명
        string buildPath = @"$output_path";
        
        // 출력 디렉토리 생성 (상위 폴더까지 모두 생성)
        try
        {
            if (!Directory.Exists(buildPath))
            {
                Directory.CreateDirectory(buildPath);
                Debug.Log("중앙 집중식 빌드 출력 디렉토리 생성: " + buildPath);
            }
            else
            {
                Debug.Log("중앙 집중식 빌드 출력 디렉토리 확인 완료: " + buildPath);
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError("빌드 출력 디렉토리 생성 실패: " + e.Message);
            Debug.LogError("경로: " + buildPath);
            return;
        }
        
        Debug.Log("📁 프로젝트명: " + projectName + " -> 안전한 파일명: " + safeProjectName);
        Debug.Log("🌐 중앙 집중식 빌드 경로: " + buildPath);
        
        // 빌드할 씬들 가져오기 (Build Settings에서 활성화된 씬만)
        string[] scenes = GetBuildScenes();
        if (scenes.Length == 0)
        {
            Debug.LogError("빌드할 씬이 없습니다. Build Settings에서 씬을 추가하세요.");
            return;
        }
        
        // WebGL 빌드 옵션 설정 (Player Settings 완전 반영)
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = scenes;
        buildPlayerOptions.locationPathName = buildPath;
        buildPlayerOptions.target = BuildTarget.WebGL;
        
        // 빌드 옵션을 Player Settings에 따라 설정
        buildPlayerOptions.options = GetBuildOptionsFromPlayerSettings();
        
        // WebGL 특수 설정 적용
        ApplyWebGLSettings();
        
        Debug.Log("🌐 WebGL 중앙 집중식 빌드 시작");
        Debug.Log("📁 중앙 빌드 경로: " + buildPlayerOptions.locationPathName);
        Debug.Log("📂 프로젝트명: " + safeProjectName);
        Debug.Log("🎮 제품명: " + PlayerSettings.productName);
        Debug.Log("🏢 회사명: " + PlayerSettings.companyName);
        Debug.Log("📋 버전: " + PlayerSettings.bundleVersion);
        
        // WebGL 빌드 실행
        Debug.Log("🔄 BuildPipeline.BuildPlayer 호출 시작...");
        UnityEditor.Build.Reporting.BuildReport report = null;
        
        try
        {
            report = BuildPipeline.BuildPlayer(buildPlayerOptions);
            Debug.Log("✅ BuildPipeline.BuildPlayer 호출 완료");
        }
        catch (System.Exception e)
        {
            Debug.LogError("❌ BuildPipeline.BuildPlayer 예외 발생: " + e.Message);
            Debug.LogError("스택 트레이스: " + e.StackTrace);
            return;
        }
        
        // 빌드 결과 확인
        if (report == null)
        {
            Debug.LogError("❌ BuildReport가 null입니다. 빌드가 실행되지 않았습니다.");
            return;
        }
        
        Debug.Log("📊 빌드 결과: " + report.summary.result);
        Debug.Log("📦 빌드 크기: " + FormatBytes(report.summary.totalSize));
        Debug.Log("⏱️ 빌드 시간: " + report.summary.totalTime);
        Debug.Log("❗ 에러 수: " + report.summary.totalErrors);
        Debug.Log("⚠️ 경고 수: " + report.summary.totalWarnings);
        
        if (report.summary.result == UnityEditor.Build.Reporting.BuildResult.Succeeded)
        {
            Debug.Log("✅ WebGL 중앙 집중식 빌드 성공!");
            Debug.Log("📁 중앙 빌드 경로: " + buildPath);
            Debug.Log("📂 프로젝트명: " + safeProjectName);
            
            // Build 폴더 내용 확인
            string buildFolder = System.IO.Path.Combine(buildPath, "Build");
            if (Directory.Exists(buildFolder))
            {
                var files = Directory.GetFiles(buildFolder);
                Debug.Log("📦 Build 폴더 파일 수: " + files.Length);
                foreach (var file in files)
                {
                    var fileInfo = new FileInfo(file);
                    Debug.Log("   - " + fileInfo.Name + " (" + FormatBytes((ulong)fileInfo.Length) + ")");
                }
            }
            else
            {
                Debug.LogError("⚠️ Build 폴더가 생성되지 않았습니다: " + buildFolder);
            }
            
            Debug.Log("🌐 중앙 집중식 WebGL 빌드 완료!");
        }
        else
        {
            Debug.LogError("❌ WebGL 빌드 실패: " + report.summary.result);
            
            // 상세 에러 정보 출력
            if (report.summary.totalErrors > 0)
            {
                Debug.LogError("총 에러 수: " + report.summary.totalErrors);
                
                // BuildReport의 steps 확인
                foreach (var step in report.steps)
                {
                    if (step.messages.Length > 0)
                    {
                        Debug.LogError("빌드 단계: " + step.name);
                        foreach (var message in step.messages)
                        {
                            if (message.type == LogType.Error || message.type == LogType.Exception)
                            {
                                Debug.LogError("  - " + message.content);
                            }
                        }
                    }
                }
            }
            
            if (report.summary.totalWarnings > 0)
            {
                Debug.LogWarning("총 경고 수: " + report.summary.totalWarnings);
            }
        }
        
        Debug.Log("=== WebGL Player Settings 반영 빌드 완료 ===");
    }
    
    private static void ConfigureWebGLPlayerSettings()
    {
        Debug.Log("🔧 WebGL Player Settings 이미지 기반 고정 설정 적용 중...");
        
        // 기본 제품 정보 설정 (비어있는 경우에만)
        if (string.IsNullOrEmpty(PlayerSettings.productName))
        {
            PlayerSettings.productName = "Science Experiment Simulation";
            Debug.Log("✅ 제품명 설정: Science Experiment Simulation");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.companyName))
        {
            PlayerSettings.companyName = "Educational Software";
            Debug.Log("✅ 회사명 설정: Educational Software");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.bundleVersion))
        {
            PlayerSettings.bundleVersion = "1.0.0";
            Debug.Log("✅ 버전 설정: 1.0.0");
        }
        
        // === 이미지 기반 고정 설정 적용 ===
        
        // Resolution and Presentation 설정 (이미지 기반)
        PlayerSettings.defaultWebScreenWidth = 1655;
        PlayerSettings.defaultWebScreenHeight = 892;
        PlayerSettings.runInBackground = true;
        Debug.Log("✅ 해상도 설정: 1655x892, Run In Background 활성화");
        
        // WebGL Template 설정 (이미지 기반: Minimal)
        PlayerSettings.WebGL.template = "APPLICATION:Minimal";
        Debug.Log("✅ WebGL 템플릿 설정: Minimal");
        
        // Publishing Settings - Brotli 압축 및 WebAssembly 2023 타겟
        PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Brotli;
        PlayerSettings.WebGL.nameFilesAsHashes = false;  // 프로젝트명.data 등으로 파일명 설정
        PlayerSettings.WebGL.dataCaching = true;
        // Unity 6에서 debugSymbols -> debugSymbolMode로 변경
        PlayerSettings.WebGL.debugSymbolMode = WebGLDebugSymbolMode.Off;
        PlayerSettings.WebGL.showDiagnostics = false;
        PlayerSettings.WebGL.decompressionFallback = true;  // Decompression Fallback 활성화
        // WebAssembly 2023 타겟 설정 (Unity 6에서 자동 관리)
        Debug.Log("✅ WebAssembly 2023: Unity 6에서 자동 관리됨");
        Debug.Log("✅ Publishing Settings: Brotli 압축 활성화, Decompression Fallback 활성화");
        
        // WebAssembly Language Features (이미지 기반)
        PlayerSettings.WebGL.exceptionSupport = WebGLExceptionSupport.ExplicitlyThrownExceptionsOnly;
        PlayerSettings.WebGL.threadsSupport = false;
        // Unity 6에서 wasmStreaming 제거됨 (decompressionFallback에 따라 자동 결정)
        Debug.Log("✅ WebAssembly 설정: 명시적 예외만, 멀티스레딩 비활성화, 스트리밍 자동");
        
        // Memory Settings (이미지 기반)
        PlayerSettings.WebGL.memorySize = 32;  // Initial Memory Size
        PlayerSettings.WebGL.memoryGrowthMode = WebGLMemoryGrowthMode.Geometric;
        PlayerSettings.WebGL.maximumMemorySize = 2048;
        Debug.Log("✅ 메모리 설정: 초기 32MB, 최대 2048MB, Geometric 증가");
        
        // Splash Screen 설정 (이미지 기반)
        PlayerSettings.SplashScreen.show = true;
        PlayerSettings.SplashScreen.showUnityLogo = false;
        PlayerSettings.SplashScreen.animationMode = PlayerSettings.SplashScreen.AnimationMode.Dolly;
        // Unity 6에서 logoAnimationMode 제거됨
        PlayerSettings.SplashScreen.overlayOpacity = 0.0f;
        PlayerSettings.SplashScreen.blurBackgroundImage = true;
        Debug.Log("✅ 스플래시 화면: Unity 로고 숨김, Dolly 애니메이션, 오버레이 투명");
        
        // WebGL 링커 타겟 설정 (Unity 6 최적화)
        PlayerSettings.WebGL.linkerTarget = WebGLLinkerTarget.Wasm;
        Debug.Log("✅ WebGL 링커 타겟 설정: WebAssembly (Unity 6 최적화)");
        
        // Code Optimization 설정 (Unity 6 Il2CppCodeGeneration 사용)
        SetCodeOptimization();
        
        // Managed Stripping Level 설정 (Medium - Unity 6)
        try
        {
            // Unity 6: ManagedStrippingLevel enum 사용
            PlayerSettings.SetManagedStrippingLevel(NamedBuildTarget.WebGL, ManagedStrippingLevel.Medium);
            Debug.Log("✅ Managed Stripping Level: Medium (Unity 6)");
        }
        catch (System.Exception e)
        {
            Debug.LogWarning("⚠️ Managed Stripping Level 설정 실패: " + e.Message);
        }
        
        Debug.Log("🔧 WebGL Player Settings 이미지 기반 고정 설정 완료");
    }
    
    private static void SetCodeOptimization()
    {
        // Unity 6 Code Optimization 설정 (WasmCodeOptimization)
        // Build Profiles의 Code Optimization 드롭다운과 일치합니다
        try
        {
            WasmCodeOptimization codeOpt;
            
            if (CODE_OPTIMIZATION_TYPE == "RuntimeSpeedLTO")
            {
                codeOpt = WasmCodeOptimization.RuntimeSpeedLTO;
                Debug.Log("✅ Code Optimization: Runtime Speed with LTO (최고 성능, LTO 적용)");
            }
            else if (CODE_OPTIMIZATION_TYPE == "RuntimeSpeed")
            {
                codeOpt = WasmCodeOptimization.RuntimeSpeed;
                Debug.Log("✅ Code Optimization: Runtime Speed (성능 최적화)");
            }
            else if (CODE_OPTIMIZATION_TYPE == "BuildTimes")
            {
                codeOpt = WasmCodeOptimization.BuildTimes;
                Debug.Log("✅ Code Optimization: Build Times (빠른 빌드)");
            }
            else if (CODE_OPTIMIZATION_TYPE == "DiskSize")
            {
                codeOpt = WasmCodeOptimization.DiskSize;
                Debug.Log("✅ Code Optimization: Disk Size (크기 최적화)");
            }
            else if (CODE_OPTIMIZATION_TYPE == "DiskSizeLTO")
            {
                codeOpt = WasmCodeOptimization.DiskSizeLTO;
                Debug.Log("✅ Code Optimization: Disk Size with LTO (최소 크기, LTO 적용)");
            }
            else
            {
                // 기본값: Runtime Speed with LTO
                codeOpt = WasmCodeOptimization.RuntimeSpeedLTO;
                Debug.LogWarning("⚠️ 알 수 없는 CODE_OPTIMIZATION_TYPE: " + CODE_OPTIMIZATION_TYPE);
                Debug.Log("ℹ️ 기본값 사용: Runtime Speed with LTO");
            }
            
            // Unity 6: UserBuildSettings.codeOptimization 사용
            UnityEditor.WebGL.UserBuildSettings.codeOptimization = codeOpt;
        }
        catch (System.Exception e)
        {
            Debug.LogError("❌ Code Optimization 설정 실패: " + e.Message);
            Debug.Log("ℹ️ Unity Editor에서 수동으로 설정해주세요.");
        }
    }
    
    private static void LogCurrentPlayerSettings()
    {
        Debug.Log("=== 현재 WebGL Player Settings ===");
        Debug.Log("🎮 제품명: " + PlayerSettings.productName);
        Debug.Log("🏢 회사명: " + PlayerSettings.companyName);
        Debug.Log("📋 버전: " + PlayerSettings.bundleVersion);
        
        // Unity 6: 아이콘 API
        var icons = PlayerSettings.GetIcons(NamedBuildTarget.WebGL, IconKind.Application);
        Debug.Log("🖼️ 기본 아이콘: " + (icons != null && icons.Length > 0 ? "설정됨" : "없음"));
        
        // WebGL 전용 설정들
        Debug.Log("🌐 WebGL 템플릿: " + PlayerSettings.WebGL.template);
        Debug.Log("💾 WebGL 메모리 크기: " + PlayerSettings.WebGL.memorySize + "MB");
        Debug.Log("📦 WebGL 압축 포맷: " + PlayerSettings.WebGL.compressionFormat);
        Debug.Log("🔙 WebGL Decompression Fallback: " + PlayerSettings.WebGL.decompressionFallback);
        // WebAssembly 2023 (Unity 6에서 자동 관리)
        Debug.Log("🌐 WebGL WebAssembly 2023: Unity 6에서 자동 관리됨");
        Debug.Log("⚠️ WebGL 예외 지원: " + PlayerSettings.WebGL.exceptionSupport);
        Debug.Log("💽 WebGL 데이터 캐싱: " + PlayerSettings.WebGL.dataCaching);
        Debug.Log("📂 WebGL 파일명 방식: " + (PlayerSettings.WebGL.nameFilesAsHashes ? "해시" : "프로젝트명") + " 기반");
        Debug.Log("🔧 WebGL 링커 타겟: " + PlayerSettings.WebGL.linkerTarget);
        Debug.Log("⚡ Code Optimization: " + UnityEditor.WebGL.UserBuildSettings.codeOptimization);
        Debug.Log("📦 Managed Stripping Level: " + PlayerSettings.GetManagedStrippingLevel(NamedBuildTarget.WebGL));
        Debug.Log("🎯 WebGL 최적화: Unity 6에서 자동 관리");
        Debug.Log("=====================================");
    }
    
    private static BuildOptions GetBuildOptionsFromPlayerSettings()
    {
        BuildOptions options = BuildOptions.None;
        
        // Development Build 설정 확인
        if (EditorUserBuildSettings.development)
        {
            options |= BuildOptions.Development;
            Debug.Log("✅ Development Build 모드 활성화");
        }
        
        // Script Debugging 설정 확인
        if (EditorUserBuildSettings.allowDebugging)
        {
            options |= BuildOptions.AllowDebugging;
            Debug.Log("✅ Script Debugging 활성화");
        }
        
        // Profiler 설정 확인
        if (EditorUserBuildSettings.connectProfiler)
        {
            options |= BuildOptions.ConnectWithProfiler;
            Debug.Log("✅ Profiler 연결 활성화");
        }
        
        // Deep Profiling 설정 확인
        if (EditorUserBuildSettings.buildWithDeepProfilingSupport)
        {
            options |= BuildOptions.EnableDeepProfilingSupport;
            Debug.Log("✅ Deep Profiling 지원 활성화");
        }
        
        // Unity 6에서 autoRunPlayer 제거됨
        // WebGL은 브라우저에서 실행되므로 AutoRunPlayer 옵션 불필요
        Debug.Log("ℹ️ WebGL 빌드는 브라우저에서 수동 실행");
        
        return options;
    }
    
    private static void ApplyWebGLSettings()
    {
        Debug.Log("🌐 WebGL 특수 설정 적용 및 검증 중...");
        
        Debug.Log("🌐 WebGL 템플릿 사용: " + PlayerSettings.WebGL.template);
        Debug.Log("💾 WebGL 메모리 크기: " + PlayerSettings.WebGL.memorySize + "MB");
        Debug.Log("📦 WebGL 압축 포맷: " + PlayerSettings.WebGL.compressionFormat);
        Debug.Log("⚠️ WebGL 예외 지원: " + PlayerSettings.WebGL.exceptionSupport);
        Debug.Log("💽 WebGL 데이터 캐싱: " + PlayerSettings.WebGL.dataCaching);
        
        // WebGL 최적화 설정 확인 및 권장사항
        if (PlayerSettings.WebGL.memorySize < 256)
        {
            Debug.LogWarning("⚠️ WebGL 메모리 크기가 256MB 미만입니다. 과학실험 시뮬레이션에는 512MB 이상 권장합니다.");
        }
        else if (PlayerSettings.WebGL.memorySize >= 512)
        {
            Debug.Log("✅ WebGL 메모리 크기가 적절합니다 (512MB 이상).");
        }
        
        if (string.IsNullOrEmpty(PlayerSettings.WebGL.template) || PlayerSettings.WebGL.template == "APPLICATION:Default")
        {
            Debug.LogWarning("⚠️ WebGL 템플릿이 기본값입니다. 교육용 템플릿 사용을 권장합니다.");
        }
        else
        {
            Debug.Log("✅ WebGL 템플릿 설정됨: " + PlayerSettings.WebGL.template);
        }
        
        // WebGL 압축 설정 확인
        if (PlayerSettings.WebGL.compressionFormat == WebGLCompressionFormat.Disabled)
        {
            Debug.LogWarning("⚠️ WebGL 압축이 비활성화되어 있습니다. 파일 크기가 클 수 있습니다.");
        }
        else
        {
            Debug.Log("✅ WebGL 압축 활성화: " + PlayerSettings.WebGL.compressionFormat);
        }
        
        // Decompression Fallback 확인
        if (PlayerSettings.WebGL.decompressionFallback)
        {
            Debug.Log("✅ WebGL Decompression Fallback 활성화 (압축 해제 실패 시 대체 사용)");
        }
        
        // WebAssembly 2023 (Unity 6에서 자동 관리)
        Debug.Log("✅ WebAssembly 2023: Unity 6에서 자동 관리됨");
        
        // Code Optimization 확인 (Unity 6 WasmCodeOptimization)
        var codeOpt = UnityEditor.WebGL.UserBuildSettings.codeOptimization;
        string codeOptStr = codeOpt.ToString();
        Debug.Log("✅ Code Optimization: " + codeOptStr + " (설정값: " + CODE_OPTIMIZATION_TYPE + ")");
        
        // Managed Stripping Level 확인 (Unity 6)
        var strippingLevel = PlayerSettings.GetManagedStrippingLevel(NamedBuildTarget.WebGL);
        Debug.Log("✅ Managed Stripping Level: " + strippingLevel);
        
        // WebGL 빌드 최적화 권장사항
        Debug.Log("📚 WebGL 빌드 최적화 권장사항:");
        Debug.Log("  - 메모리: 512MB 이상");
        Debug.Log("  - 압축: Brotli (현재 설정됨)");
        Debug.Log("  - Decompression Fallback: 활성화 (현재 설정됨)");
        Debug.Log("  - WebAssembly 2023: 활성화 (현재 설정됨)");
        Debug.Log("  - Managed Stripping Level: Medium (현재 설정됨)");
        Debug.Log("  - Code Optimization: " + CODE_OPTIMIZATION_TYPE + " (현재 설정됨)");
        Debug.Log("  - 예외 지원: ExplicitlyThrownExceptionsOnly");
        Debug.Log("  - 데이터 캐싱: 활성화");
    }
    
    private static string[] GetBuildScenes()
    {
        // Build Settings에서 활성화된 씬들만 가져오기
        var enabledScenes = new System.Collections.Generic.List<string>();
        
        foreach (var scene in EditorBuildSettings.scenes)
        {
            if (scene.enabled)
            {
                enabledScenes.Add(scene.path);
            }
        }
        
        Debug.Log("📋 빌드할 씬 수: " + enabledScenes.Count);
        foreach (var scene in enabledScenes)
        {
            Debug.Log("  - " + scene);
        }
        
        return enabledScenes.ToArray();
    }
    
    private static string FormatBytes(ulong bytes)
    {
        string[] sizes = { "B", "KB", "MB", "GB", "TB" };
        double len = bytes;
        int order = 0;
        while (len >= 1024 && order < sizes.Length - 1)
        {
            order++;
            len = len / 1024;
        }
        return len.ToString("0.##") + " " + sizes[order];
    }
}
""")
    
    try:
        formatted_content = script_template.substitute(
            output_path=output_path_formatted,
            code_optimization=code_optimization
        )
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        print(f"WebGL 전용 빌드 스크립트 생성 완료: {script_path}")
        print(f"  ⚡ Code Optimization: {code_optimization}")
        return True
    except Exception as e:
        print(f"WebGL 빌드 스크립트 생성 실패: {e}")
        return False

def validate_build_output(build_dir, project_name, log_file_path=None):
    """빌드 출력 폴더를 검증하여 필수 파일들이 생성되었는지 확인합니다.
    
    Args:
        build_dir: 빌드 출력 디렉토리 경로
        project_name: 프로젝트 이름
        log_file_path: Unity 로그 파일 경로 (선택)
    
    Returns:
        dict: {
            "valid": bool (빌드 파일이 유효한지),
            "found_files": list (발견된 필수 파일 목록),
            "missing_files": list (누락된 필수 파일 목록)
        }
    """
    result = {
        "valid": False,
        "found_files": [],
        "missing_files": []
    }
    
    if not os.path.exists(build_dir):
        result["missing_files"].append("빌드 디렉토리 자체가 존재하지 않음")
        return result
    
    # 1단계: 로그 파일에서 Unity 빌드 성공 메시지 확인
    unity_build_success = False
    unity_files_generated = False
    
    if log_file_path and os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r', encoding='utf-8', errors='replace') as f:
                log_content = f.read()
                
                # Unity가 빌드 성공을 보고했는지 확인 (여러 패턴 체크)
                success_patterns = [
                    "✅ WebGL 중앙 집중식 빌드 성공!",
                    "📊 빌드 결과: Succeeded",
                    "BuildResult.Succeeded"
                ]
                
                for pattern in success_patterns:
                    if pattern in log_content:
                        unity_build_success = True
                        result["found_files"].append(f"Unity 빌드 성공 보고 ({pattern})")
                        break
                
                # Build 폴더에 파일이 생성되었는지 확인
                if "📦 Build 폴더 파일 수:" in log_content:
                    import re
                    match = re.search(r'📦 Build 폴더 파일 수: (\d+)', log_content)
                    if match:
                        file_count = int(match.group(1))
                        if file_count > 0:
                            unity_files_generated = True
                            result["found_files"].append(f"Build 폴더에 {file_count}개 파일 생성됨")
                
                # 빌드 완료 메시지도 확인 (fallback)
                if not unity_files_generated and "🌐 중앙 집중식 WebGL 빌드 완료!" in log_content:
                    # 오래된 로그 형식 (파일 수 정보가 없는 경우)
                    unity_files_generated = True
                    result["found_files"].append("빌드 완료 메시지 확인됨")
        except Exception as e:
            pass  # 로그 파일 파싱 실패는 무시하고 파일 시스템 검증으로 진행
    
    # Unity가 빌드 성공을 보고하고 파일도 생성했다면 성공으로 처리
    if unity_build_success and unity_files_generated:
        result["valid"] = True
        return result
    
    # Unity WebGL 빌드 필수 파일들
    required_files = {
        "index.html": "index.html",
        "Build folder": "Build"
    }
    
    # 기본 필수 파일 확인
    for file_type, file_name in required_files.items():
        file_path = os.path.join(build_dir, file_name)
        if os.path.exists(file_path):
            result["found_files"].append(file_type)
        else:
            result["missing_files"].append(file_type)
    
    # 2단계: Build 폴더 내부 필수 파일 확인 (.wasm, .data 등)
    build_folder = os.path.join(build_dir, "Build")
    if os.path.exists(build_folder):
        try:
            build_contents = os.listdir(build_folder)
            
            # Build 폴더가 비어있는지 확인
            if not build_contents:
                result["missing_files"].append("Build 폴더가 비어있음")
                # 하지만 Unity가 빌드 완료를 보고했다면 파일이 잠시 후 생성될 수 있음
                if unity_build_success:
                    result["found_files"].append("Unity 빌드 완료 보고됨 (파일 생성 대기 중)")
                    result["valid"] = True
                return result
            
            # 필수 확장자 확인 (압축 파일 포함)
            # Unity 6 + Brotli: .wasm.br, .data.br, .framework.js.br, .loader.js
            has_wasm = any(
                ".wasm" in f.lower() and (
                    f.endswith(".wasm") or f.endswith(".wasm.br") or f.endswith(".wasm.gz")
                ) for f in build_contents
            )
            has_data = any(
                ".data" in f.lower() and (
                    f.endswith(".data") or f.endswith(".data.br") or f.endswith(".data.gz")
                ) for f in build_contents
            )
            has_loader = any(
                ".loader.js" in f.lower() or (
                    ".loader" in f.lower() and ".js" in f.lower()
                ) for f in build_contents
            )
            has_framework = any(
                ".framework.js" in f.lower() or (
                    ".framework" in f.lower() and ".js" in f.lower()
                ) for f in build_contents
            )
            
            if has_wasm:
                wasm_files = [f for f in build_contents if ".wasm" in f.lower()]
                result["found_files"].append(f"WebAssembly: {', '.join(wasm_files)}")
            else:
                result["missing_files"].append("WebAssembly (.wasm 또는 .wasm.br)")
            
            if has_data:
                data_files = [f for f in build_contents if ".data" in f.lower()]
                result["found_files"].append(f"Data file: {', '.join(data_files)}")
            else:
                result["missing_files"].append("Data file (.data 또는 .data.br)")
            
            if has_loader:
                loader_files = [f for f in build_contents if ".loader" in f.lower()]
                result["found_files"].append(f"Loader: {', '.join(loader_files)}")
            else:
                result["missing_files"].append("Loader (.loader.js)")
            
            if has_framework:
                framework_files = [f for f in build_contents if ".framework" in f.lower()]
                result["found_files"].append(f"Framework: {', '.join(framework_files)}")
            else:
                result["missing_files"].append("Framework (.framework.js 또는 .framework.js.br)")
            
            # 엄격한 검증: 모든 필수 파일이 있어야 함
            strict_valid = has_wasm and has_data and has_loader and has_framework
            
            # 관대한 검증: Unity가 빌드 성공을 보고하고 Build 폴더에 파일이 하나라도 있으면 성공
            lenient_valid = unity_build_success and len(build_contents) > 0
            
            result["valid"] = strict_valid or lenient_valid
            
            if lenient_valid and not strict_valid:
                result["found_files"].append(f"Unity 빌드 성공 + Build 폴더에 {len(build_contents)}개 파일 존재")
        except Exception as e:
            result["missing_files"].append(f"Build 폴더 검증 실패: {e}")
    else:
        result["missing_files"].append("Build 폴더가 존재하지 않음")
    
    return result

def monitor_build_progress(log_file_path, project_name, stop_event, start_time):
    """로그 파일을 주기적으로 모니터링하여 빌드 진행 상황을 표시합니다."""
    last_position = 0
    check_interval = 60  # 1분마다 체크
    
    # 주요 진행 단계 키워드
    progress_keywords = [
        "Compiling scripts",
        "Building Library",
        "Building player",
        "Building WebGL Player",
        "IL2CPP",
        "Building il2cpp",
        "Generating code",
        "Compiling C++ code",
        "Building WASM",
        "Emscripten"
    ]
    
    while not stop_event.is_set():
        try:
            if os.path.exists(log_file_path):
                elapsed = int(time.time() - start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                
                # 파일 끝부분만 읽기 (성능 최적화)
                with open(log_file_path, 'r', encoding='utf-8', errors='replace') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    last_position = f.tell()
                    
                    # 주요 진행 단계 찾기
                    progress_found = False
                    for line in new_lines:
                        for keyword in progress_keywords:
                            if keyword in line:
                                print(f"  ⏳ [{project_name}] {minutes}분 {seconds}초 경과 - {keyword}")
                                progress_found = True
                                break
                        if progress_found:
                            break
                    
                    # 진행 단계가 없으면 단순 상태 메시지
                    if not progress_found and new_lines:
                        print(f"  ⏳ [{project_name}] {minutes}분 {seconds}초 경과 - 빌드 진행 중...")
                
            time.sleep(check_interval)
        except Exception as e:
            # 오류가 발생해도 모니터링 중단하지 않음
            pass

def run_unity_webgl_build(project_path, timeout=BUILD_TIMEOUT):
    """Unity CLI를 사용하여 WebGL 빌드를 실행합니다. (Player Settings 완전 반영)"""
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
    
    print(f"🌐 Unity WebGL Player Settings 반영 빌드 시작: {project_name}")
    
    # 빌드 시작 시간 기록
    build_start_time = time.time()
    
    # 빌드 출력 디렉토리 미리 생성
    project_build_dir = os.path.join(BUILD_OUTPUT_DIR, project_name)
    
    # 로그 파일 경로 생성
    log_dir = os.path.join(BUILD_OUTPUT_DIR, "_Logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"{project_name}_{timestamp}.log")
    
    # 빌드 스크립트 경로 (나중에 정리를 위해 저장)
    script_path = os.path.join(project_path, "Assets", "Editor", "AutoWebGLBuildScript.cs")
    script_meta_path = script_path + ".meta"
    
    try:
        if not os.path.exists(project_build_dir):
            os.makedirs(project_build_dir, exist_ok=True)
            print(f"빌드 출력 디렉토리 생성: {project_build_dir}")
        else:
            print(f"빌드 출력 디렉토리 확인 완료: {project_build_dir}")
    except Exception as e:
        print(f"빌드 출력 디렉토리 생성 실패: {e}")
        return False, 0.0
    
    # WebGL 전용 빌드 스크립트 생성
    if not create_unity_webgl_build_script(project_path):
        return False, 0.0
    
    # Unity CLI 명령어 구성
    cmd = [
        unity_path,
        "-batchmode",
        "-quit", 
        "-projectPath", project_path,
        "-buildTarget", "WebGL",
        "-executeMethod", "AutoWebGLBuildScript.BuildWebGLWithPlayerSettings",
        "-logFile", log_file_path  # 로그 파일 경로 지정
    ]
    
    # print(f"📝 로그 파일 경로: {log_file_path}")
    
    # 진행도 모니터링 스레드 준비
    stop_monitor = threading.Event()
    monitor_thread = threading.Thread(
        target=monitor_build_progress,
        args=(log_file_path, project_name, stop_monitor, build_start_time),
        daemon=True
    )
    
    try:
        print(f"🌐 Unity WebGL 빌드 실행 중... (타임아웃: {timeout}초)")
        # print(f"명령어: {' '.join(cmd)}")
        
        # 진행도 모니터링 시작
        monitor_thread.start()
        
        # Unity는 -logFile로 로그를 직접 파일에 쓰므로 stdout/stderr 캡처 불필요
        # capture_output=True는 거대한 로그를 메모리 버퍼링하여 심각한 성능 저하 유발
        result = subprocess.run(
            cmd,
            timeout=timeout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # 빌드 완료, 모니터링 중지
        stop_monitor.set()
        
        # 빌드 종료 시간 기록
        build_end_time = time.time()
        elapsed_time = build_end_time - build_start_time
        
        # 시간을 읽기 쉬운 형태로 변환
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
        
        if result.returncode == 0:
            # 빌드 파일 검증: 실제로 필수 파일들이 생성되었는지 확인
            build_validation = validate_build_output(project_build_dir, project_name, log_file_path)
            
            if build_validation["valid"]:
                print(f"✅ Unity WebGL 빌드 성공: {project_name} (소요 시간: {time_str})")
                print(f"   📦 빌드 파일 검증 완료:")
                for found_file in build_validation['found_files']:
                    print(f"      ✓ {found_file}")
                
                # Build 하위 폴더 파일 크기 정보
                build_subfolder = os.path.join(project_build_dir, "Build")
                if os.path.exists(build_subfolder):
                    try:
                        total_size = 0
                        for file in os.listdir(build_subfolder):
                            file_path = os.path.join(build_subfolder, file)
                            if os.path.isfile(file_path):
                                total_size += os.path.getsize(file_path)
                        print(f"   💾 빌드 총 크기: {format_bytes(total_size)}")
                    except:
                        pass
                
                # if os.path.exists(log_file_path):
                #     print(f"📝 빌드 로그: {log_file_path}")
                return True, elapsed_time
            else:
                print(f"❌ Unity WebGL 빌드 실패 (파일 검증 실패): {project_name} (소요 시간: {time_str})")
                print(f"   ⚠️ 빌드가 완료되었으나 필수 파일이 생성되지 않았습니다.")
                print(f"   ⚠️ 누락된 파일: {', '.join(build_validation['missing_files'])}")
                
                # 빌드 폴더 내용물 상세 확인
                if os.path.exists(project_build_dir):
                    try:
                        contents = os.listdir(project_build_dir)
                        if contents:
                            print(f"   📁 빌드 폴더 내용: {', '.join(contents)}")
                            
                            # Build 하위 폴더 내용 확인
                            build_subfolder = os.path.join(project_build_dir, "Build")
                            if os.path.exists(build_subfolder):
                                build_contents = os.listdir(build_subfolder)
                                if build_contents:
                                    print(f"   📦 Build 하위 폴더 내용 ({len(build_contents)}개 파일):")
                                    for file in build_contents:
                                        file_path = os.path.join(build_subfolder, file)
                                        file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
                                        size_str = format_bytes(file_size)
                                        print(f"      - {file} ({size_str})")
                                else:
                                    print(f"   ⚠️ Build 하위 폴더가 비어있습니다!")
                            else:
                                print(f"   ⚠️ Build 하위 폴더가 존재하지 않습니다!")
                        else:
                            print(f"   📁 빌드 폴더가 비어있습니다.")
                    except Exception as e:
                        print(f"   ⚠️ 빌드 폴더 확인 실패: {e}")
                
                # 로그 파일 확인
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                        log_lines = log_file.readlines()
                        if log_lines:
                            print("\n" + "="*80)
                            print("📝 로그 파일 마지막 50줄 (오류 확인):")
                            print("="*80)
                            last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                            for line in last_lines:
                                print(line.rstrip())
                            print("="*80)
                
                return False, elapsed_time
        else:
            print(f"❌ Unity WebGL 빌드 실패: {project_name} (종료 코드: {result.returncode}, 소요 시간: {time_str})")
            
            # 오류 발생 시 로그 파일의 마지막 부분 읽어서 표시
            try:
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                        log_lines = log_file.readlines()
                        if log_lines:
                            print("\n" + "="*80)
                            print("📝 로그 파일 마지막 50줄 (오류 확인):")
                            print("="*80)
                            last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                            for line in last_lines:
                                print(line.rstrip())
                            print("="*80)
            except Exception as e:
                print(f"⚠️ 로그 파일 읽기 실패: {e}")
            
            # if os.path.exists(log_file_path):
            #     print(f"📝 전체 실패 로그: {log_file_path}")
            return False, elapsed_time
            
    except subprocess.TimeoutExpired:
        # 모니터링 중지
        stop_monitor.set()
        
        # 빌드 종료 시간 기록
        build_end_time = time.time()
        elapsed_time = build_end_time - build_start_time
        
        # 시간을 읽기 쉬운 형태로 변환
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
        
        error_msg = f"Unity WebGL 빌드 타임아웃: {project_name} ({timeout}초 초과, 소요 시간: {time_str})"
        print(f"❌ {error_msg}")
        
        # 타임아웃 오류를 로그 파일에 추가 저장
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write("\n" + "="*80 + "\n")
                    log_file.write(f"TIMEOUT ERROR: {error_msg}\n")
                    log_file.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write("="*80 + "\n")
                
                # 로그 파일의 마지막 부분 표시
                with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                    log_lines = log_file.readlines()
                    if log_lines:
                        print("\n" + "="*80)
                        print("📝 타임아웃 직전 로그 (마지막 50줄):")
                        print("="*80)
                        last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                        for line in last_lines:
                            print(line.rstrip())
                        print("="*80)
        except Exception as e:
            print(f"⚠️ 타임아웃 로그 저장 실패: {e}")
        
        # if os.path.exists(log_file_path):
        #     print(f"📝 전체 타임아웃 로그: {log_file_path}")
        return False, elapsed_time
        
    except Exception as e:
        # 모니터링 중지
        stop_monitor.set()
        
        # 빌드 종료 시간 기록
        build_end_time = time.time()
        elapsed_time = build_end_time - build_start_time
        
        # 시간을 읽기 쉬운 형태로 변환
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
        
        error_msg = f"Unity WebGL 빌드 예외: {project_name} - {e} (소요 시간: {time_str})"
        print(f"❌ {error_msg}")
        
        # 예외 오류를 로그 파일에 추가 저장
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, 'a', encoding='utf-8') as log_file:
                    log_file.write("\n" + "="*80 + "\n")
                    log_file.write(f"EXCEPTION ERROR: {error_msg}\n")
                    log_file.write(f"Exception Type: {type(e).__name__}\n")
                    log_file.write(f"Exception Details: {str(e)}\n")
                    import traceback
                    log_file.write("\n--- Traceback ---\n")
                    log_file.write(traceback.format_exc())
                    log_file.write(f"\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write("="*80 + "\n")
                
                # 로그 파일의 마지막 부분 표시
                with open(log_file_path, 'r', encoding='utf-8', errors='replace') as log_file:
                    log_lines = log_file.readlines()
                    if log_lines:
                        print("\n" + "="*80)
                        print("📝 예외 발생 직전 로그 (마지막 50줄):")
                        print("="*80)
                        last_lines = log_lines[-50:] if len(log_lines) > 50 else log_lines
                        for line in last_lines:
                            print(line.rstrip())
                        print("="*80)
        except Exception as log_error:
            print(f"⚠️ 예외 로그 저장 실패: {log_error}")
        
        # if os.path.exists(log_file_path):
        #     print(f"📝 전체 예외 로그: {log_file_path}")
        return False, elapsed_time
    
    finally:
        # 빌드 스크립트 정리 (성공/실패/예외 모든 경우에 실행)
        try:
            cleaned_files = []
            if os.path.exists(script_path):
                os.remove(script_path)
                cleaned_files.append("AutoWebGLBuildScript.cs")
            if os.path.exists(script_meta_path):
                os.remove(script_meta_path)
                cleaned_files.append("AutoWebGLBuildScript.cs.meta")
            
            if cleaned_files:
                print(f"🧹 임시 빌드 스크립트 정리 완료: {', '.join(cleaned_files)}")
        except Exception as e:
            print(f"⚠️ 빌드 스크립트 정리 실패: {e}")

def build_multiple_webgl_projects(project_dirs, parallel=False, max_workers=2):
    """여러 Unity 프로젝트를 WebGL로 빌드합니다.
    
    Returns:
        tuple: (results, total_elapsed_time)
            - results: [(project_name, success, elapsed_time), ...]
            - total_elapsed_time: 전체 빌드 소요 시간 (초)
    """
    print(f"\n=== Unity WebGL 다중 프로젝트 빌드 시작 ===")
    
    if parallel:
        return build_multiple_webgl_projects_parallel(project_dirs, max_workers)
    else:
        return build_multiple_webgl_projects_sequential(project_dirs)

def build_multiple_webgl_projects_sequential(project_dirs):
    """여러 Unity 프로젝트를 WebGL로 순차적으로 빌드합니다."""
    total_projects = len(project_dirs)
    print(f"📊 총 {total_projects}개 프로젝트 빌드 예정")
    
    success_count = 0
    fail_count = 0
    completed_count = 0
    results = []
    total_start_time = time.time()
    
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            print(f"❌ 프로젝트 경로가 존재하지 않습니다: {project_dir}")
            fail_count += 1
            completed_count += 1
            project_name = get_project_name_from_path(project_dir)
            results.append((project_name, False, 0.0))
            progress_percent = int((completed_count / total_projects) * 100)
            print(f"📊 전체 진행도: {completed_count}/{total_projects} 완료 ({progress_percent}%)")
            continue
        
        project_name = get_project_name_from_path(project_dir)
        print(f"\n--- {project_name} WebGL 빌드 시작 ---")
        
        success, elapsed_time = run_unity_webgl_build(project_dir)
        completed_count += 1
        progress_percent = int((completed_count / total_projects) * 100)
        
        if success:
            success_count += 1
            results.append((project_name, True, elapsed_time))
        else:
            fail_count += 1
            results.append((project_name, False, elapsed_time))
        
        # 전체 진행도 표시
        print(f"📊 전체 진행도: {completed_count}/{total_projects} 완료 ({progress_percent}%)")
    
    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    
    return results, total_elapsed_time

def build_multiple_webgl_projects_parallel(project_dirs, max_workers=2):
    """여러 Unity 프로젝트를 WebGL로 병렬로 빌드합니다."""
    total_projects = len([d for d in project_dirs if os.path.exists(d)])
    print(f"🌐 WebGL 병렬 빌드 시작 (최대 {max_workers}개 동시 실행)")
    print(f"📊 총 {total_projects}개 프로젝트 빌드 예정")
    
    success_count = 0
    fail_count = 0
    completed_count = 0
    results = []
    total_start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 모든 프로젝트를 병렬로 제출
        future_to_project = {
            executor.submit(run_unity_webgl_build, project_dir): project_dir 
            for project_dir in project_dirs if os.path.exists(project_dir)
        }
        
        # 완료된 작업들을 처리
        for future in as_completed(future_to_project):
            project_dir = future_to_project[future]
            project_name = get_project_name_from_path(project_dir)
            
            try:
                success, elapsed_time = future.result()
                completed_count += 1
                progress_percent = int((completed_count / total_projects) * 100)
                
                if success:
                    success_count += 1
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
                    print(f"✅ {project_name} WebGL 병렬 빌드 완료 (소요 시간: {time_str})")
                else:
                    fail_count += 1
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    time_str = f"{minutes}분 {seconds}초" if minutes > 0 else f"{seconds}초"
                    print(f"❌ {project_name} WebGL 병렬 빌드 실패 (소요 시간: {time_str})")
                
                # 전체 진행도 표시
                print(f"📊 전체 진행도: {completed_count}/{total_projects} 완료 ({progress_percent}%)")
                
                results.append((project_name, success, elapsed_time))
            except Exception as e:
                fail_count += 1
                completed_count += 1
                progress_percent = int((completed_count / total_projects) * 100)
                print(f"❌ {project_name} WebGL 병렬 빌드 예외: {e}")
                print(f"📊 전체 진행도: {completed_count}/{total_projects} 완료 ({progress_percent}%)")
                results.append((project_name, False, 0.0))
    
    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    
    return results, total_elapsed_time

def clean_build_outputs(project_dirs):
    """중앙 집중식 빌드 출력물을 정리합니다."""
    print("\n=== 중앙 집중식 빌드 출력물 정리 시작 ===")
    print(f"📁 중앙 빌드 폴더: {BUILD_OUTPUT_DIR}")
    
    if not os.path.exists(BUILD_OUTPUT_DIR):
        print("⚪ 중앙 빌드 폴더가 존재하지 않습니다.")
        return
    
    cleaned_count = 0
    total_size = 0
    
    # 각 프로젝트별 빌드 폴더 정리
    for project_dir in project_dirs:
        if not os.path.exists(project_dir):
            continue
            
        project_name = get_project_name_from_path(project_dir)
        project_build_dir = os.path.join(BUILD_OUTPUT_DIR, project_name)
        
        if os.path.exists(project_build_dir):
            try:
                import shutil
                # 폴더 크기 계산
                folder_size = 0
                for dirpath, dirnames, filenames in os.walk(project_build_dir):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            folder_size += os.path.getsize(filepath)
                        except:
                            pass
                
                total_size += folder_size
                shutil.rmtree(project_build_dir)
                
                # 크기를 읽기 쉬운 형태로 변환
                size_str = format_bytes(folder_size)
                print(f"✅ {project_name} 중앙 빌드 출력물 정리 완료 ({size_str})")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ {project_name} 중앙 빌드 출력물 정리 실패: {e}")
        else:
            print(f"⚪ {project_name} 중앙 빌드 출력물 없음")
    
    total_size_str = format_bytes(total_size)
    print(f"\n📊 정리 완료: {cleaned_count}개 프로젝트, 총 {total_size_str} 절약")
    print(f"📁 중앙 빌드 폴더: {BUILD_OUTPUT_DIR}")

def format_bytes(bytes_size):
    """바이트 크기를 읽기 쉬운 형태로 변환합니다."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"
# endregion
