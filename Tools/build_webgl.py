import subprocess
import os

# Unity Editor 실행 파일 경로 (환경에 맞게 수정)
UNITY_PATH = r"C:\Program Files\Unity\Hub\Editor\2022.3.0f1\Editor\Unity.exe"

# Unity 프로젝트 경로 (환경에 맞게 수정)
PROJECT_PATH = r"E:\3.1.2.2_ClassifyAnimals"

# 빌드에 사용할 C# Editor 스크립트의 static 메서드명
BUILD_METHOD = "AutoWebGLBuild.BuildWebGL"

# 로그 파일 저장 경로 (선택)
LOG_PATH = os.path.join(PROJECT_PATH, "unity_build.log")

# Unity 명령줄 인자 구성
cmd = [
    UNITY_PATH,
    "-batchmode",
    "-nographics",
    "-quit",
    "-projectPath", PROJECT_PATH,
    "-executeMethod", BUILD_METHOD,
    "-logFile", LOG_PATH
]

# 빌드 실행
print("Unity WebGL 자동 빌드를 시작합니다...")
result = subprocess.run(cmd)

if result.returncode == 0:
    print("✅ Unity WebGL 빌드가 정상적으로 완료되었습니다.")
else:
    print("❌ Unity WebGL 빌드에 실패했습니다. 로그를 확인하세요:", LOG_PATH)