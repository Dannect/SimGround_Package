import subprocess
import os

# 경로와 프로젝트 위치 기입 필요

UNITY_PATH = r"D:\Unity\6000.0.30f1\Editor\Unity.exe"
PROJECT_PATH = r"E:\3.1.2.2_ClassifyAnimals"
BUILD_METHOD = "AutoWebGLBuild.BuildWebGL"
LOG_PATH = os.path.join(PROJECT_PATH, "unity_build.log")

cmd = [
    UNITY_PATH,
    "-batchmode",
    "-nographics",
    "-quit",
    "-projectPath", PROJECT_PATH,
    "-executeMethod", BUILD_METHOD,
    "-logFile", LOG_PATH
]

print("Unity WebGL 자동 빌드를 시작합니다...")
result = subprocess.run(cmd)

if result.returncode == 0:
    print("✅ Unity WebGL 빌드가 정상적으로 완료되었습니다.")
else:
    print("❌ Unity WebGL 빌드에 실패했습니다. 로그를 확인하세요:", LOG_PATH)