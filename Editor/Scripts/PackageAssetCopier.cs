using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;
using System.IO;
using System.Collections.Generic;
using UnityEditor.SceneManagement;

[InitializeOnLoad]
public class PackageAssetCopier
{
    static PackageAssetCopier()
    {
        EditorApplication.delayCall += CopyFilesFromPackage;
    }

    public static void CopyFilesFromPackage()
    {
        MergePrefabWithButtonEvents();
    }

    public static void MergePrefabWithButtonEvents()
    {
        string packagePrefabPath = "Packages/com.dannect.toolkit/Runtime/Prefabs/Warning_Pop.prefab";
        string projectPrefabPath = "Assets/04.Prefabs/Warning/Prefabs/Warning_Pop.prefab";

        // 1. 기존 프리팹의 Button OnClick 정보 저장
        Dictionary<string, List<(Object, string)>> buttonEventDict = new Dictionary<string, List<(Object, string)>>();
        GameObject oldPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(projectPrefabPath);
        if (oldPrefab != null)
        {
            var oldButtons = oldPrefab.GetComponentsInChildren<Button>(true);
            foreach (var btn in oldButtons)
            {
                var onClick = btn.onClick;
                int eventCount = onClick.GetPersistentEventCount();
                var eventList = new List<(Object, string)>();
                for (int i = 0; i < eventCount; i++)
                {
                    var target = onClick.GetPersistentTarget(i);
                    var methodName = onClick.GetPersistentMethodName(i);
                    if (target != null && !string.IsNullOrEmpty(methodName))
                    {
                        eventList.Add((target, methodName));
                    }
                }
                buttonEventDict[btn.name] = eventList;
            }
        }

        // 2. 패키지 프리팹을 임시 씬에 인스턴스화
        var tempScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
        GameObject tempInstance = (GameObject)PrefabUtility.InstantiatePrefab(
            AssetDatabase.LoadAssetAtPath<GameObject>(packagePrefabPath), tempScene);

        // 3. 임시 인스턴스를 프로젝트(Assets/)에 저장
        Directory.CreateDirectory(Path.GetDirectoryName(projectPrefabPath));
        PrefabUtility.SaveAsPrefabAsset(tempInstance, projectPrefabPath);
        GameObject.DestroyImmediate(tempInstance);
        EditorSceneManager.CloseScene(tempScene, true);

        // 4. 프로젝트 프리팹을 다시 로드 (이제 읽기/쓰기 가능)
        GameObject projectPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(projectPrefabPath);
        var prefabInstance = PrefabUtility.InstantiatePrefab(projectPrefab) as GameObject;

        // 5. Button의 OnClick을 복원
        var newButtons = prefabInstance.GetComponentsInChildren<Button>(true);
        foreach (var btn in newButtons)
        {
            if (buttonEventDict.TryGetValue(btn.name, out var eventList))
            {
                // 기존 이벤트를 모두 제거
                int removeCount = btn.onClick.GetPersistentEventCount();
                for (int j = removeCount - 1; j >= 0; j--)
                {
                    UnityEditor.Events.UnityEventTools.RemovePersistentListener(btn.onClick, j);
                }

                // 기존 이벤트를 복원
                foreach (var (target, methodName) in eventList)
                {
                    if (target != null && !string.IsNullOrEmpty(methodName))
                    {
                        var method = target.GetType().GetMethod(methodName, System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic);
                        if (method != null)
                        {
                            UnityAction action = (UnityAction)System.Delegate.CreateDelegate(typeof(UnityAction), target, method);
                            UnityEditor.Events.UnityEventTools.AddPersistentListener(btn.onClick, action);
                        }
                    }
                }
            }
        }



        Directory.CreateDirectory(Path.GetDirectoryName(absProjectPath));
        File.Copy(absPackagePath, absProjectPath, true);
        AssetDatabase.Refresh();


        AssetDatabase.Refresh();
        Debug.Log("패키지 프리팹을 병합하여 프로젝트로 복사 완료! (Button OnClick 이벤트 Inspector에 100% 유지)");
    }
}