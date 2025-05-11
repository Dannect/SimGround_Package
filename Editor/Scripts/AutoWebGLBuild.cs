using UnityEditor;
using System;
using System.IO;
using System.Linq;


public class AutoWebGLBuild
{
    public static void BuildWebGL()
    {
        // Build Settings에 등록된 씬 목록 자동 수집
        var scenes = EditorBuildSettings.scenes
            .Where(s => s.enabled)
            .Select(s => s.path)
            .ToArray();

        // 빌드 파일명에 날짜/시간 추가
        string timeStamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
        string buildFolder = "Build/WebGL";
        string buildName = "Build";
        string buildPath = Path.Combine(buildFolder, buildName + ".html");

        // 빌드 폴더가 없으면 생성
        if (!Directory.Exists(buildFolder))
            Directory.CreateDirectory(buildFolder);

        // WebGL 빌드 실행
        var report = BuildPipeline.BuildPlayer(
            scenes,
            buildPath,
            BuildTarget.WebGL,
            BuildOptions.None
        );

        if (report.summary.result == UnityEditor.Build.Reporting.BuildResult.Succeeded)
        {
            UnityEngine.Debug.Log($"WebGL 빌드 성공!\n출력 경로: {buildFolder}");
        }
        else
        {
            UnityEngine.Debug.LogError($"WebGL 빌드 실패: {report.summary.result}");
        }
    }
}
