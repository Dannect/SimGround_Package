using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;
using System.IO;
using System.Collections.Generic;
using UnityEditor.Events;

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

        // 2. 기존 프리팹의 Button OnClick 정보 저장 및 로그 출력
        Dictionary<string, Button.ButtonClickedEvent> buttonEventDict = new Dictionary<string, Button.ButtonClickedEvent>();
        if (oldPrefab != null)
        {
            var oldButtons = oldPrefab.GetComponentsInChildren<Button>(true);
            foreach (var btn in oldButtons)
            {
                var onClick = btn.onClick;
                int eventCount = onClick.GetPersistentEventCount();
                for (int i = 0; i < eventCount; i++)
                {
                    var target = onClick.GetPersistentTarget(i);
                    var methodName = onClick.GetPersistentMethodName(i);
                    if (target != null && !string.IsNullOrEmpty(methodName))
                    {
                        Debug.Log($"[Button OnClick] 버튼: {btn.name}, 타겟 오브젝트: {target.name}, 메소드: {methodName}", btn.gameObject);
                    }
                }
                buttonEventDict[btn.name] = CloneButtonClickedEvent(btn.onClick);
            }
        }

        // 3. 새 프리팹 인스턴스 생성
        GameObject newInstance = (GameObject)PrefabUtility.InstantiatePrefab(newPrefab);

        // 4. Button에 기존 OnClick 이벤트 복사
        var newButtons = newInstance.GetComponentsInChildren<Button>(true);
        foreach (var btn in newButtons)
        {
            if (buttonEventDict.TryGetValue(btn.name, out var oldEvent))
            {
                // 기존 이벤트를 모두 제거
                int persistentCount = btn.onClick.GetPersistentEventCount();
                for (int i = persistentCount - 1; i >= 0; i--)
                {
                    UnityEditor.Events.UnityEventTools.RemovePersistentListener(btn.onClick, i);
                }

                int count = oldEvent.GetPersistentEventCount();
                for (int i = 0; i < count; i++)
                {
                    var target = oldEvent.GetPersistentTarget(i);
                    var methodName = oldEvent.GetPersistentMethodName(i);
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

        // 5. 기존 프리팹을 새 인스턴스로 교체
        Directory.CreateDirectory(Path.GetDirectoryName(projectPrefabPath));
        PrefabUtility.SaveAsPrefabAsset(newInstance, projectPrefabPath);
        GameObject.DestroyImmediate(newInstance);

        AssetDatabase.Refresh();
        Debug.Log("패키지 프리팹을 병합하여 프로젝트로 복사 완료! (Button OnClick 이벤트 유지)");
    }

    // ButtonClickedEvent 복제 함수
    private static Button.ButtonClickedEvent CloneButtonClickedEvent(Button.ButtonClickedEvent source)
    {
        var clone = new Button.ButtonClickedEvent();
        int count = source.GetPersistentEventCount();
        for (int i = 0; i < count; i++)
        {
            var target = source.GetPersistentTarget(i);
            var methodName = source.GetPersistentMethodName(i);
            if (target != null && !string.IsNullOrEmpty(methodName))
            {
                var method = target.GetType().GetMethod(methodName, System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic);
                if (method != null)
                {
                    UnityAction action = (UnityAction)System.Delegate.CreateDelegate(typeof(UnityAction), target, method);
                    UnityEditor.Events.UnityEventTools.AddPersistentListener(clone, action);
                }
            }
        }
        return clone;
    }
}