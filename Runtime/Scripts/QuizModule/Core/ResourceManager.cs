using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;
using UnityEngine.ResourceManagement.ResourceLocations;
using Object = UnityEngine.Object;

namespace Quiz
{
    public class ResourceManager : MonoBehaviour
    {
        private Dictionary<string, Object> _resources = new Dictionary<string, Object>();

        public IEnumerator Init()
        {
            // Addressables 초기화
            var initHandle = Addressables.InitializeAsync();
            yield return initHandle;

            // 카탈로그 업데이트 체크
            var checkForUpdateHandle = Addressables.CheckForCatalogUpdates(true);
            yield return checkForUpdateHandle;

            // 외부 카탈로그 로드
            var catalogHandle = Addressables.LoadContentCatalogAsync(
                "https://kr.object.ncloudstorage.com/simground-static/WebGL/catalog_1.0.0.json", true);
            yield return catalogHandle;

            LoadAsset();
            Debug.Log("ResourceManager Init Complete");
        }

        #region Load Resource
        public T Load<T>(string key) where T : Object
        {
            if (_resources.TryGetValue(key, out Object resource))
                return resource as T;

            return null;
        }

        public GameObject Instantiate(string key, Transform parent = null)
        {
            GameObject prefab = Load<GameObject>(key);
            if (prefab == null)
            {
                Debug.LogError($"Failed to load prefab : {key}");
                return null;
            }

            GameObject go = Instantiate(prefab);

            go.transform.SetParent(parent, false);
            go.name = prefab.name;

            return go;
        }

        public void Destroy(GameObject go)
        {
            if (go == null)
                return;

            Object.Destroy(go);
        }
        #endregion

        #region Addressable
        public void LoadAsset()
        {
            // Download_Asset();
            StartCoroutine(LoadAllAssets<GameObject>("QuizBase"));
        }

        AsyncOperationHandle<GameObject> handle;
        public IEnumerator LoadAllAssets<T>(string label) where T : UnityEngine.Object
        {
            // 키에 해당하는 리소스 위치를 먼저 가져온다
            var locationsHandle = Addressables.LoadResourceLocationsAsync(label, typeof(T));
            yield return locationsHandle;

            if (locationsHandle.Status == AsyncOperationStatus.Succeeded && locationsHandle.Result.Count > 0)
            {
                Debug.Log("locationsHandle.Result.Count : " + locationsHandle.Result.Count);

                foreach (var location in locationsHandle.Result)
                {
                    handle = Addressables.LoadAssetAsync<GameObject>(location);
                    yield return handle;

                    if (handle.Status == AsyncOperationStatus.Succeeded)
                    {
                        _resources.Add(handle.Result.name, handle.Result);
                        Debug.Log("handle.Result.name : " + handle.Result.name);
                    }
                }

            }
            else
            {
                Debug.LogError("리소스 위치를 찾을 수 없습니다: " + label);
            }

            // 리소스 위치 핸들 해제
            Addressables.Release(locationsHandle);
        }

        private void OnDestroy()
        {
            Addressables.Release(handle);
        }
        #endregion
    }
}