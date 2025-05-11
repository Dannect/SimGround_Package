using UnityEditor;
using UnityEngine;
using System.IO;

[InitializeOnLoad]
public class PackageAssetCopier
{
    static PackageAssetCopier()
    {
        EditorApplication.delayCall += CopyFilesFromPackage;
    }

    public static void CopyFilesFromPackage()
    {
        // 프리팹 복사
        CopyAssetFromPackage(
            "Packages/com.dannect.toolkit/Runtime/Prefabs/Warning_Pop.prefab",
            "Assets/04.Prefabs/Warning/Prefabs/Warning_Pop.prefab",
            "프리팹",
            true
        );

    }

    private static void CopyAssetFromPackage(string packagePath, string projectPath, string assetType, bool overwrite = true)
    {
        string absPackagePath = Path.GetFullPath(packagePath);
        string absProjectPath = Path.GetFullPath(projectPath);

        if (!File.Exists(absPackagePath))
        {
            Debug.LogWarning($"패키지 {assetType}을(를) 찾을 수 없습니다(아직 Import 중일 수 있음): {absPackagePath}");
            return;
        }

        // 대상 파일이 이미 존재하는 경우
        if (File.Exists(absProjectPath))
        {
            if (!overwrite)
            {
                Debug.Log($"프로젝트에 이미 {assetType}이(가) 존재합니다. 건너뜁니다: {absProjectPath}");
                return;
            }
            else
            {
                // 기존 파일 삭제
                File.Delete(absProjectPath);
                AssetDatabase.Refresh();
                Debug.Log($"기존 {assetType} 파일을 삭제했습니다: {absProjectPath}");
            }
        }

        Directory.CreateDirectory(Path.GetDirectoryName(absProjectPath));
        File.Copy(absPackagePath, absProjectPath, true);
        AssetDatabase.Refresh();

        Debug.Log($"패키지 {assetType}을(를) 프로젝트로 복사 완료!");
    }
}