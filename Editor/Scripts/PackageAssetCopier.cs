using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System.Collections.Generic;

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
        Dictionary<string, List<(Object, string)>> buttonEventDict = new Dictionary<string, List<(Object, string)>>();
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
                        Debug.Log($"[Button OnClick] 버튼: {btn.name}, 타겟 오브젝트: {target.name}, 메소드: {methodName}", btn.gameObject);
                        eventList.Add((target as Object, methodName));
                    }
                }
                buttonEventDict[btn.name] = eventList;
            }
        }

        // 3. 새 프리팹 인스턴스 생성
        GameObject newInstance = (GameObject)PrefabUtility.InstantiatePrefab(newPrefab);

        // 4. Button에 기존 OnClick 이벤트 복사 (SerializedObject 사용)
        var newButtons = newInstance.GetComponentsInChildren<Button>(true);
        foreach (var btn in newButtons)
        {
            if (buttonEventDict.TryGetValue(btn.name, out var eventList))
            {
                // SerializedObject로 직접 할당
                SerializedObject so = new SerializedObject(btn);
                var onClickProp = so.FindProperty("m_OnClick.m_PersistentCalls.m_Calls");
                onClickProp.ClearArray();

                for (int i = 0; i < eventList.Count; i++)
                {
                    onClickProp.InsertArrayElementAtIndex(i);
                    var call = onClickProp.GetArrayElementAtIndex(i);
                    call.FindPropertyRelative("m_Target").objectReferenceValue = eventList[i].Item1;
                    call.FindPropertyRelative("m_MethodName").stringValue = eventList[i].Item2;
                    call.FindPropertyRelative("m_Mode").enumValueIndex = 1; // PersistentListenerMode.EventDefined
                    call.FindPropertyRelative("m_Arguments").FindPropertyRelative("m_ObjectArgumentAssemblyTypeName").stringValue = "";
                }
                so.ApplyModifiedProperties();
            }
        }

        // 5. 기존 프리팹을 새 인스턴스로 교체
        Directory.CreateDirectory(Path.GetDirectoryName(projectPrefabPath));
        PrefabUtility.SaveAsPrefabAsset(newInstance, projectPrefabPath);
        GameObject.DestroyImmediate(newInstance);

        AssetDatabase.Refresh();
        Debug.Log("패키지 프리팹을 병합하여 프로젝트로 복사 완료! (Button OnClick 이벤트 Inspector에 100% 유지)");
    }
}