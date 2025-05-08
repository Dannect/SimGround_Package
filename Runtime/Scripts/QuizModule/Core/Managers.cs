using System.Collections;
using UnityEngine;
using UnityEngine.AddressableAssets;

namespace Quiz
{
    public class Managers : MonoBehaviour
    {
        public static bool Initialized { get; set; } = false;
        public static Managers s_instance;
        public static Managers Instance { get { return s_instance; } }

        private ResourceManager _resource;
        private QuizManager _quiz;
        private SystemManager _system;
        public static ResourceManager Resource { get { return Instance?._resource; } }
        public static QuizManager Quiz { get { return Instance?._quiz; } }
        public static SystemManager System { get { return Instance?._system; } }


        private void Awake()
        {
            Application.targetFrameRate = 60;
            Init();
            _resource = GetComponentInChildren<ResourceManager>();
            _quiz = GetComponentInChildren<QuizManager>();
            _system = GetComponentInChildren<SystemManager>();
            StartCoroutine(_resource.Init());
        }

        public static void Init()
        {
            Initialized = true;

            GameObject go = GameObject.Find("Managers");

            if (go == null)
            {
                go = new GameObject { name = "Managers" };
                go.AddComponent<Managers>();
            }

            DontDestroyOnLoad(go);

            s_instance = go.GetComponent<Managers>();

        }
    }
}