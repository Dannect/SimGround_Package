"""
Unity 프로젝트 자동화 도구 설정 및 상수 정의
"""
import os


class Config:
    """전체 설정 및 상수 클래스"""
    # 프로젝트 경로
    PROJECT_DIRS = [
        ### 3학년
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.1.2_Card",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.1.3_Balance",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.1.4_ElectricScale",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.1.5_SpringScale",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.1.6_LeverPower",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.2.2_ClassifyAnimals_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.2.3_AroundAnimal_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.2.4_UnderGroundAnimals_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.2.5_UnderWaterAnimals_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.2.6_DesertAndNorthAnimals_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.3.2_SchoolPlants_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.3.4_MountainPlants_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.3.5_WaterPlant_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.3.6_DesertPlants_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.4.3_ButterFlyLifeCycle_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.4.5_GlowSeed",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.1.4.6_GlowPlant",
        
        # ### 4학년
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.1.2_BasicMagnet",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.1.3_AttachSaftyPinMagnet",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.1.4_CreateSaftyPinMagnet",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.1.5_CompassMagnet",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.1.6_AluminumMagnet",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.1.7_DailyLifeMagnet",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.2.2_StateOfWater_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.2.4_FreezeAndMelt_v2",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.2.5_EvaporationAndBoil",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.2.7_ColdObjectSurface",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.2.8_GetWater",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.3.2_ChangeLand",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.3.5_MarshmallowVolcano",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.3.6_BasaltGraniteFeature_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.3.7_VolcanicInfluence_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.4.1_MicroScopeGuide",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.4.2_MushroomAndMoldFeature_v2",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.1.4.4_SpirogyraParameciumFeature_v2",
        
        ### 5학년
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.1.3_TemperatureMeasurement",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.1.5_ContactHeatFlow",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.1.6_HeatFlowInSolids",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.1.8_HeatFlowInFluid",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.1.9_HeatFlowInGases",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.2.3_CelestialObservation",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.2.4_ExploreThePlanets",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.2.5_ScaleThePlanets",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.2.6_PlanetDistances",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.2.8_NorthernConstellations",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.2.9_StellarNavigation",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.3.2_SolubilityObservation",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.3.3_SolubilityWeight",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.3.4_SolubilityComparison",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.3.5_SolubilityFactors",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.3.6_CompareConcentration",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.3.7_ConcentrationTool",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.4.3_ObservingParamecium",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.1.4.5_ObservingMushrooms",
        
        ### 6학년
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.1.2_SunAndMoon",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.1.3_EarthMove",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.1.5_SeasonalConstellations",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.1.6_ConstellationsWithEarthMove",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.1.7_MoonShapeEachDays",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.2.2_MakeOxygen",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.2.4_MakeCarbonDioxide",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.2.6_ThermalExpansionGases",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.2.7_VolumeChangeOfGas",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.2.10_TemperatureMeasuringDevice",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.3.3_StructureAndFunctionOfRoots",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.3.4_StructureAndFunctionOfStems",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.3.5_StructureAndFunctionOfLeaves",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.3.6_IdentifyPhotosynthesisProducts",
        r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.2_ObservingRainbowMadeWithPrism",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.3_LightPassingThroughWaterOrGlass",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.5_ConvexLensLight",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.1.4.6_ConvexLensObservation",
        
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.1.6_AbioticFactors",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.2.7_WindFormationModel",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.2.2_SolarAltitudeShadowLengthTemperature",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.2.2_LandSeaComparison",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.1.2_MaterialProperties",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.1.5_SolidLiquidChanges",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.2.5_WaterHeating",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.3.2_SoundAndVibration",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.3.3_CompareLoudAndSoftSound",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.3.4_HighAndLowSound",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.3.6_SoundPropagation",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\3.2.4.7_DiseasePrevention",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.2.3.2_ObserveChangeWeightAir",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.2.3.3_ChangeGasVolumeByTemperature",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\4.2.3.4_PressureChangeGasVolume",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.2.2_WetAndDryBulbHygrometer",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.2.4_DewAndFogFormation"
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.2.5_RainSnowFormation",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.2.6_AirWeightByTemperature",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.4.2_ClassifySolutions",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.4.3_ClassifySolutionsWithIndicators",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.4.4_CreateIndicators",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.4.6_AcidBaseProperties",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\5.2.4.7_MixAcidAndBaseSolutions",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.1.1_MakeRobot",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.1.2_TurnOnTheLightBulb",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.1.3_CompareBrightnessOfBulbs",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.1.5_MakeElectromagnet",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.1.6_CompareElectromagnetAndPermanentMagnet",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.2.6_SolarAltitudeTempSimulator",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.2.7_SolarAltitudeBySeasons",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.3.1_FireExtinguisherPutOutCandles",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.3.2_ObservingPhenomenaSubstanceBurns",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.3.3_ConditionsRequiredSubstanceBurn",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.3.5_SubstancesProducedAfterCombustion",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.3.6_MethodsOfExtinguishingFire",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.4.3_StructureAndFunctionOfTheDigestiveSystem",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.4.4_StructureAndFunctionOfTheCirculatorySystem",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.4.5_StructureAndFunctionOfTheRespiratorySystem",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\6.2.4.6_StructureAndFunctionOfTheExcretoryOrgans",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\High_1.1.2.1_ElementFormation",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\High_1.1.2.2_IonicBondingCoualentBonding",
        # r"C:\Users\wkzkx\Desktop\Lim\GitHub\High_2.2.1.1_ObservePropertiesOfAcidAndBase"
    ]
    
    # Git 설정
    GIT_BASE_URL = "https://github.com/Dannect/"
    DEFAULT_BRANCH = "main"
    DEV_BRANCH = "dev"
    
    # Unity 설정
    UNITY_EDITOR_PATH = r"C:\Program Files\Unity\Hub\Editor\6000.0.59f2\Editor\Unity.exe"
    UNITY_TIMEOUT = 300
    BUILD_TIMEOUT = 7200
    BUILD_OUTPUT_DIR = r"C:\Users\wkzkx\Desktop\Lim\GitHub\Build"
    
    # WebGL 빌드 설정
    # Code Optimization (Unity 6.0의 WasmCodeOptimization)
    # 사용 가능한 옵션:
    #   - "BuildTimes": 빠른 빌드 시간 (개발용)
    #   - "RuntimeSpeed": 성능 최적화
    #   - "RuntimeSpeedLTO": 성능 최적화 + LTO (권장, 최고 성능)
    #   - "DiskSize": 크기 최적화
    #   - "DiskSizeLTO": 크기 최적화 + LTO (최소 크기)
    WEBGL_CODE_OPTIMIZATION = "RuntimeSpeed"
    
    # 패키지 설정
    GIT_PACKAGES = {
        "com.dannect.toolkit": "https://github.com/Dannect/SimGround_Package.git"
    }
    
    # 커밋 메시지 템플릿
    COMMIT_MESSAGES = {
        "package_update": "FEAT: Unity 패키지 업데이트 및 자동 설정 적용",
        "system_manager_update": "FEAT: SystemManager 메소드 추가 및 기능 확장",
        "webgl_build": "BUILD: WebGL 빌드 설정 및 출력 파일 생성",
        "auto_general": "CHORE: 자동화 도구를 통한 프로젝트 업데이트",
        "batch_process": "CHORE: Unity 배치 모드 자동 처리 완료",
        "full_automation": "FEAT: 완전 자동화 처리 (패키지 + 설정 + 빌드)"
    }


def get_unity_projects_from_directory(base_dir):
    """지정된 디렉토리에서 Unity 프로젝트들을 자동으로 찾습니다."""
    unity_projects = []
    
    if not os.path.exists(base_dir):
        print(f"기본 디렉토리가 존재하지 않습니다: {base_dir}")
        return unity_projects
    
    try:
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                project_settings = os.path.join(item_path, "ProjectSettings")
                assets_folder = os.path.join(item_path, "Assets")
                
                if os.path.exists(project_settings) and os.path.exists(assets_folder):
                    unity_projects.append(item_path)
                    print(f"Unity 프로젝트 발견: {item}")
    
    except Exception as e:
        print(f"디렉토리 스캔 오류: {e}")
    
    return unity_projects


# 호환성을 위한 전역 변수들 (기존 코드와의 호환성 유지)
project_dirs = Config.PROJECT_DIRS
git_packages = Config.GIT_PACKAGES
GIT_BASE_URL = Config.GIT_BASE_URL
DEFAULT_BRANCH = Config.DEFAULT_BRANCH
DEV_BRANCH = Config.DEV_BRANCH
COMMIT_MESSAGES = Config.COMMIT_MESSAGES
UNITY_EDITOR_PATH = Config.UNITY_EDITOR_PATH
UNITY_TIMEOUT = Config.UNITY_TIMEOUT
BUILD_TIMEOUT = Config.BUILD_TIMEOUT
BUILD_OUTPUT_DIR = Config.BUILD_OUTPUT_DIR
WEBGL_CODE_OPTIMIZATION = Config.WEBGL_CODE_OPTIMIZATION

