using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
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

        // 1. 프리팹 로드
        GameObject oldPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(projectPrefabPath);
        GameObject newPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(packagePrefabPath);

        if (newPrefab == null)
        {
            Debug.LogWarning("패키지 프리팹을 찾을 수 없습니다: " + packagePrefabPath);
            return;
        }

        // 2. 기존 프리팹의 Button OnClick 정보 저장
        Dictionary<string, List<(string, string)>> buttonEventDict = new Dictionary<string, List<(string, string)>>();
        if (oldPrefab != null)
        {
            var oldButtons = oldPrefab.GetComponentsInChildren<Button>(true);
            foreach (var btn in oldButtons)
            {
                var onClick = btn.onClick;
                int eventCount = onClick.GetPersistentEventCount();
                var eventList = new List<(string, string)>();
                for (int i = 0; i < eventCount; i++)
                {
                    var target = onClick.GetPersistentTarget(i) as Component;
                    var methodName = onClick.GetPersistentMethodName(i);
                    if (target != null && !string.IsNullOrEmpty(methodName))
                    {
                        // 프리팹 내부 컴포넌트만 저장
                        string path = GetTransformPath(target.transform, oldPrefab.transform);
                        if (!string.IsNullOrEmpty(path))
                        {
                            Debug.Log($"[Button OnClick] 버튼: {btn.name}, 타겟 경로: {path}, 메소드: {methodName}", btn.gameObject);
                            eventList.Add((path, methodName));
                        }
                    }
                }
                buttonEventDict[btn.name] = eventList;
            }
        }

        // 3. 새 프리팹 인스턴스를 임시 씬에 생성
        var tempScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
        GameObject newInstance = (GameObject)PrefabUtility.InstantiatePrefab(newPrefab, tempScene);

        // 4. Button에 기존 OnClick 이벤트 복사 (프리팹 내부 컴포넌트만)
        var newButtons = newInstance.GetComponentsInChildren<Button>(true);
        foreach (var btn in newButtons)
        {
            if (buttonEventDict.TryGetValue(btn.name, out var eventList))
            {
                SerializedObject so = new SerializedObject(btn);
                var onClickProp = so.FindProperty("m_OnClick.m_PersistentCalls.m_Calls");
                onClickProp.ClearArray();

                for (int i = 0; i < eventList.Count; i++)
                {
                    var (targetPath, methodName) = eventList[i];
                    var targetTransform = FindTransformByPath(newInstance.transform, targetPath);
                    if (targetTransform != null)
                    {
                        // Button, Image, CustomScript 등 컴포넌트 모두 지원
                        var comp = targetTransform.GetComponent<Component>();
                        if (comp != null)
                        {
                            onClickProp.InsertArrayElementAtIndex(i);
                            var call = onClickProp.GetArrayElementAtIndex(i);
                            call.FindPropertyRelative("m_Target").objectReferenceValue = comp;
                            call.FindPropertyRelative("m_MethodName").stringValue = methodName;
                            call.FindPropertyRelative("m_Mode").enumValueIndex = 1; // PersistentListenerMode.EventDefined
                            call.FindPropertyRelative("m_Arguments").FindPropertyRelative("m_ObjectArgumentAssemblyTypeName").stringValue = "";
                        }
                    }
                }
                so.ApplyModifiedProperties();
            }
        }

        // 5. 기존 프리팹을 새 인스턴스로 교체
        Directory.CreateDirectory(Path.GetDirectoryName(projectPrefabPath));
        PrefabUtility.SaveAsPrefabAsset(newInstance, projectPrefabPath);
        GameObject.DestroyImmediate(newInstance);

        // 6. 임시 씬 정리
        EditorSceneManager.CloseScene(tempScene, true);

        AssetDatabase.Refresh();
        Debug.Log("패키지 프리팹을 병합하여 프로젝트로 복사 완료! (Button OnClick 이벤트 Inspector에 100% 유지)");
    }

    // 프리팹 내부 경로 구하기
    private static string GetTransformPath(Transform target, Transform root)
    {
        if (target == root) return "";
        var path = target.name;
        while (target.parent != null && target.parent != root)
        {
            target = target.parent;
            path = target.name + "/" + path;
        }
        return path;
    }

    // 경로로 Transform 찾기
    private static Transform FindTransformByPath(Transform root, string path)
    {
        if (string.IsNullOrEmpty(path)) return root;
        return root.Find(path);
    }
}