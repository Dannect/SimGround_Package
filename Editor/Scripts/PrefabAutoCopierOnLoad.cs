using UnityEditor;
using UnityEngine;
using System.IO;

[InitializeOnLoad]
public class PrefabAutoCopierOnLoad
{
    static PrefabAutoCopierOnLoad()
    {
        EditorApplication.delayCall += CopyPrefabFromPackage;
    }

    public static void CopyPrefabFromPackage()
    {
        string packagePrefabPath = "Packages/com.dannect.toolkit/Runtime/Prefabs/Warning_Pop.prefab";
        
        string projectPrefabPath = "Assets/04.Prefabs/Warning/Prefabs/Warning_Pop.prefab";

        string absPackagePath = Path.GetFullPath(packagePrefabPath);
        string absProjectPath = Path.GetFullPath(projectPrefabPath);

        if (!File.Exists(absPackagePath))
        {
            Debug.LogWarning("패키지 프리팹을 찾을 수 없습니다(아직 Import 중일 수 있음): " + absPackagePath);
            return;
        }

        Directory.CreateDirectory(Path.GetDirectoryName(absProjectPath));
        File.Copy(absPackagePath, absProjectPath, true);
        AssetDatabase.Refresh();

        Debug.Log("패키지 프리팹을 프로젝트로 복사 완료!");
    }
}