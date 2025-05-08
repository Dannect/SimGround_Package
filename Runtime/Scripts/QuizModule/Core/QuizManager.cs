using System;
using UnityEngine;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.UI;
namespace Quiz
{
    public class QuizManager : MonoBehaviour
    {
        public CourseContentDetail quizData;
        public List<QuizByStageAndStep> solveQuizDataList;
        public Queue<object> quizQueue = new Queue<object>();
        private List<GameObject> quizList = new List<GameObject>();
        private int currentQuizIndex = 0;
        public Transform rootCanvas;
        public GameObject quizBase;
        public bool isStudent;
        public IQuiz currentQuiz;
        public void SetQuizData(CourseContentDetail quizData)
        {
            this.quizData = quizData;
            SortQuizData();
            // isStudent = true;
        }
        public void SetSolveQuizData(List<QuizByStageAndStep> solveQuizDataList)
        {
            this.solveQuizDataList = solveQuizDataList;
            Debug.Log("solveQuizDataList: " + solveQuizDataList.Count);
        }
        // 타입별로 QuizType 매핑
        private Dictionary<System.Type, System.Type> quizTypeMap = new Dictionary<System.Type, System.Type>
        {
            { typeof(ShortQuizData), typeof(ShortWordQuizType) },
            { typeof(MultipleChoiceQuizData), typeof(MultipleChoiceQuizType) },
            { typeof(OxChoiceQuizData), typeof(OXChoiceQuizType) },
            { typeof(ClassificationQuizData), typeof(ClassificationQuizType) },
            { typeof(BlankQuizData), typeof(BlankQuizType) },
        };
        void Start()
        {
            if (rootCanvas == null)
            {
                // Canvas 생성
                GameObject canvasObj = new GameObject("MainCanvas");
                Canvas canvas = canvasObj.AddComponent<Canvas>();
                canvas.renderMode = RenderMode.ScreenSpaceOverlay;
                // Canvas Scaler 설정
                CanvasScaler scaler = canvasObj.AddComponent<CanvasScaler>();
                scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
                scaler.referenceResolution = new Vector2(1655, 892);
                scaler.matchWidthOrHeight = 0f; // 가로/세로 비율 중간값으로 설정
                // Graphic Raycaster 추가
                canvasObj.AddComponent<GraphicRaycaster>();
                rootCanvas = canvasObj.transform;
            }
            else
            {
                rootCanvas = GameObject.Find("MainCanvas").transform;

            }
        }
        public void SortQuizData()
        {
            // 모든 퀴즈를 하나의 리스트로 합친다
            List<object> allQuizzes = new List<object>();
            if (quizData == null) return;
            if (quizData.multipleChoiceQuizzes != null)
                allQuizzes.AddRange(quizData.multipleChoiceQuizzes);
            if (quizData.oxChoiceQuizzes != null)
                allQuizzes.AddRange(quizData.oxChoiceQuizzes);
            if (quizData.shortQuizzes != null)
                allQuizzes.AddRange(quizData.shortQuizzes);
            // if (quizData.classificationQuizzes != null)
            //     allQuizzes.AddRange(quizData.classificationQuizzes);
            if (quizData.blankQuizzes != null)
                allQuizzes.AddRange(quizData.blankQuizzes);
            // quizStep 기준으로 정렬
            var sorted = allQuizzes.OrderBy(q =>
            {
                // 각 타입별로 quizStep 프로퍼티를 가져온다
                if (q is MultipleChoiceQuizData mcq) return mcq.quizStep;
                if (q is OxChoiceQuizData ox) return ox.quizStep;
                if (q is ShortQuizData sq) return sq.quizStep;
                if (q is ClassificationQuizData cq) return cq.quizStep;
                if (q is BlankQuizData bq) return bq.quizStep;
                return int.MaxValue;
            });
            // Queue에 삽입
            quizQueue = new Queue<object>(sorted);
            Debug.Log("quizQueueCount: " + quizQueue.Count);
        }
        public void SetFeedback(string feedback)
        {
            currentQuiz.ResponseFeedback(feedback);
        }
        public void BuildQuizUI()
        {
            if (quizQueue.Count == 0) return;
            quizBase = Managers.Resource.Instantiate("QuizBase", rootCanvas);
            quizBase.transform.SetParent(rootCanvas);
            quizList.Add(quizBase);
            object quizData = quizQueue.Dequeue();
            System.Type dataType = quizData.GetType();
            foreach (var item in quizBase.GetComponentsInChildren<QuizBase>())
            {
                item.gameObject.SetActive(false);
            }
            if (quizTypeMap.TryGetValue(dataType, out System.Type quizTypeScript))
            {
                quizBase.GetComponentInChildren(quizTypeScript, true).gameObject.SetActive(true);
                IQuiz quiz = (IQuiz)quizBase.GetComponentInChildren(quizTypeScript);
                QuizBase qb = (QuizBase)quizBase.GetComponentInChildren(quizTypeScript);
                // 데이터 세팅 및 UI 빌드
                quiz.BuildQuiz();
                quiz.SetQuizData(quizData);
                //학생일 때
                if (isStudent)
                {
                    for (int i = 0; i < solveQuizDataList.Count; i++)
                    {
                        if (solveQuizDataList[i].shortQuiz != null && solveQuizDataList[i].shortQuiz.step == qb.quizStep)
                        {
                            quiz.SetSolvedQuizData(solveQuizDataList[i].shortQuiz);
                            Debug.Log(solveQuizDataList[i].shortQuiz.isCorrect);
                            Debug.Log(JsonUtility.ToJson(solveQuizDataList[i].shortQuiz));
                        }
                        else if (solveQuizDataList[i].multipleChoiceQuiz != null && solveQuizDataList[i].multipleChoiceQuiz.step == qb.quizStep)
                        {
                            quiz.SetSolvedQuizData(solveQuizDataList[i].multipleChoiceQuiz);
                            Debug.Log(JsonUtility.ToJson(solveQuizDataList[i].multipleChoiceQuiz));
                        }
                        else if (solveQuizDataList[i].oxQuiz != null && solveQuizDataList[i].oxQuiz.step == qb.quizStep)
                        {
                            quiz.SetSolvedQuizData(solveQuizDataList[i].oxQuiz);
                            Debug.Log(JsonUtility.ToJson(solveQuizDataList[i].oxQuiz));
                        }
                        else if (solveQuizDataList[i].classificationQuiz != null && solveQuizDataList[i].classificationQuiz.step == qb.quizStep)
                        {
                            quiz.SetSolvedQuizData(solveQuizDataList[i].classificationQuiz);
                            Debug.Log(JsonUtility.ToJson(solveQuizDataList[i].classificationQuiz));
                        }
                        else if (solveQuizDataList[i].blankQuiz != null && solveQuizDataList[i].blankQuiz.step == qb.quizStep)
                        {
                            quiz.SetSolvedQuizData(solveQuizDataList[i].blankQuiz);
                            Debug.Log(JsonUtility.ToJson(solveQuizDataList[i].blankQuiz));
                        }
                    }
                }
                //선생님일 때
                else
                {
                    quiz.ShowTeacherView();
                }
                currentQuizIndex = quizList.Count - 1;
                if (currentQuizIndex == 0)
                {
                    Managers.System.CallNotifyReactApp("EXPERIMENTSTART");
                }
            }
            else
            {
                Debug.LogError("지원하지 않는 퀴즈 타입: " + dataType.Name);
            }
        }
        public void OpenNextQuiz()
        {
            Debug.Log("OpenNextQuiz");
            if (currentQuizIndex < quizList.Count - 1)
            {
                quizList[currentQuizIndex].SetActive(false);
                currentQuizIndex++;
                quizList[currentQuizIndex].SetActive(true);
            }
            else
            {
                // 마지막 퀴즈일 경우
                if (quizQueue.Count == 0) return;
                if (quizList.Count != 0)
                {
                    quizList[currentQuizIndex].SetActive(false);
                }
                BuildQuizUI();
                Managers.System.CallNotifyReactApp("EXPERIMENTEND");
            }
        }
        public void OpenPreviousQuiz()
        {
            Debug.Log("OpenPreviousQuiz");
            if (currentQuizIndex > 0)
            {
                quizList[currentQuizIndex].SetActive(false);
                currentQuizIndex--;
                quizList[currentQuizIndex].SetActive(true);
                Managers.System.CallNotifyReactApp("EXPERIMENTSTART");
            }
        }
        // ShortQuiz 테스트 데이터를 생성해서 큐에 넣고 BuildQuizUI를 호출하는 함수
        public void TestShortQuiz()
        {
            // 테스트용 ShortQuiz 데이터 생성
            ShortQuizData testQuiz = new ShortQuizData
            {
                id = 1,
                uuid = "2397e919-f102-4301-9671-be878beb265e",
                quizStep = 5,
                question = "화산활동 모형에서 {{}}은 마그마를 표현한 것이다",
                rubric = "화산활동 모형에대한 질문"
            };
            // 큐 초기화 및 데이터 삽입
            quizQueue.Enqueue(testQuiz);
            // 퀴즈 UI 생성
            BuildQuizUI();
        }
    }
}