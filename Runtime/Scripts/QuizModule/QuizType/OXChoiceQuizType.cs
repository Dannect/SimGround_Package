using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Quiz
{
    public class OXChoiceQuizType : QuizBase, IQuiz
    {
        [SerializeField] private TMP_Text questionText;
        [SerializeField] private Button[] oxPanelButtons;
        [SerializeField] private Image[] oxRadioImages;
        [SerializeField] private Sprite[] radioSprites;
        [SerializeField] private Sprite[] oxSprites;
        private int answer = -1;
        private int correctAnswer = -1;
        private OxChoiceQuizData quizData;
        public void BuildQuiz()
        {
            InitQuizUI();
            submitButton.onClick.RemoveAllListeners();
            submitButton.onClick.AddListener(SubmitQuiz);
            ResetImages();
            answer = -1;
            isCheckTime = true;
        }

        void Start()
        {
            //test
            // OxQuiz quiz = new OxQuiz
            // {
            //     studentId = 345,
            //     step = 2,
            //     question = "화산은 위험할까요",
            //     firstOption = "네",
            //     secondOption = "아니오",
            //     firstFeedback = "정답입니다",
            //     secondFeedback = "오답",
            //     activityStage = "EXPERIMENT",
            //     id = null,
            //     studentAnswer = "1",
            //     isCorrect = true,
            //     correctAnswer = "1",
            //     submittedAt = null,
            //     timeTaken = 10
            // };
            // SetSolvedQuizData(quiz);
        }
        public void SetQuizData(object quizData)
        {
            this.quizData = (OxChoiceQuizData)quizData;
            id = this.quizData.id;
            uuid = this.quizData.uuid;
            quizStep = this.quizData.quizStep;
            question = this.quizData.question;
            questionText.text = this.quizData.question;
            correctAnswer = this.quizData.correctOption;
        }

        public void SubmitQuiz()
        {
            //제출 webRequest 호출
            submitButton.interactable = false;
            isCheckTime = false;
            QuizAnswerData submitData = new QuizAnswerData
            {
                quizType = "OX_CHOICE",
                quizId = id,
                studentAnswer = answer.ToString(),
                timeTaken = (int)timeTaken
            };

            QuizSubmitData quizSubmitData = new QuizSubmitData
            {
                type = "WEB_REQUEST",
                data = submitData
            };
            // JSON으로 직렬화
            string jsonData = JsonUtility.ToJson(quizSubmitData);
            Debug.Log("jsonData: " + jsonData);
            Managers.System.CallNotifyReactApp(jsonData);
            ResponseFeedback("");
            nextObject.SetActive(true);

        }

        public void SetSolvedQuizData(object quizData)
        {
            if (quizData is OxQuiz data)
            {
                if (data.studentAnswer == null) return;

                answer = int.Parse(data.studentAnswer);
                OnOXButtonsClick(answer - 1);
                ResponseFeedback("");
                nextObject.SetActive(true);
            }
        }
        public void ResponseFeedback(string responseData)
        {
            string feedbackText = "";
            if (answer == 1)
                feedbackText = quizData.firstFeedback;
            else if (answer == 2)
                feedbackText = quizData.secondFeedback;

            bool isCorrect = answer == correctAnswer ? true : false;

            feedback.SetFeedback(feedbackText, isCorrect);
            feedback.gameObject.SetActive(true);
            submitObject.SetActive(false);
        }
        public void ShowTeacherView()
        {
            answer = correctAnswer;
            OnOXButtonsClick(correctAnswer - 1);
            ResponseFeedback("");
        }
        public void OnOXButtonsClick(int index)
        {
            if (answer == -1)
            {
                submitButton.interactable = true;
            }
            answer = index + 1;

            for (int i = 0; i < 2; i++)
            {
                oxRadioImages[i].sprite = radioSprites[0];
            }

            oxRadioImages[index].sprite = radioSprites[1];

            // 선택한 패널 버튼 이미지 변경
            if (index < oxPanelButtons.Length)
            {
                oxPanelButtons[index].image.sprite = oxSprites[index]; // 선택한 버튼은 index
            }

            if (index == 0)
            {
                oxPanelButtons[0].image.sprite = oxSprites[0];
                oxPanelButtons[1].image.sprite = oxSprites[3];

            }
            else
            {
                oxPanelButtons[0].image.sprite = oxSprites[2];
                oxPanelButtons[1].image.sprite = oxSprites[1];
            }
        }

        private void ResetImages()
        {
            for (int i = 0; i < 2; i++)
            {
                oxRadioImages[i].sprite = radioSprites[0];
                oxPanelButtons[i].image.sprite = oxSprites[i];
            }
        }


        // private IEnumerator SubmitQuizCoroutine()
        // {
        //     // 데이터 객체 생성
        //     Debug.Log("classId: " + Managers.Quiz.classId);
        //     Debug.Log("quizId: " + 1);
        //     Debug.Log("studentAnswer: " + answerInputField.text);
        //     Debug.Log("timeTaken: " + timeTaken);

        //     QuizSubmitStringData submitData = new QuizSubmitStringData
        //     {
        //         classId = int.Parse(Managers.Quiz.classId),
        //         quizId = id,
        //         studentAnswer = answerInputField.text,
        //         timeTaken = (int)timeTaken
        //     };

        //     // JSON으로 직렬화
        //     string jsonData = JsonUtility.ToJson(submitData);
        //     byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);

        //     using (UnityWebRequest www = new UnityWebRequest(Managers.Quiz.hostURL + "class/short-quiz", "POST"))
        //     {
        //         www.uploadHandler = new UploadHandlerRaw(bodyRaw);
        //         www.downloadHandler = new DownloadHandlerBuffer();
        //         www.SetRequestHeader("Content-Type", "application/json");
        //         www.useHttpContinue = true;
        //         www.SetRequestHeader("withCredentials", "true");

        //         yield return www.SendWebRequest();

        //         if (www.result != UnityWebRequest.Result.Success)
        //         {
        //             Debug.LogError(www.error);
        //         }
        //         else
        //         {
        //             Debug.Log("Form upload complete!");
        //             Debug.Log(www.downloadHandler.text);
        //             QuizResponse response = JsonUtility.FromJson<QuizResponse>(www.downloadHandler.text);
        //             ActiveFeedbackUI(response.data.feedback, response.data.isCorrect);
        //             feedback.gameObject.SetActive(true);
        //             nextObject.SetActive(true);
        //             submitObject.SetActive(false);
        //             gameObject.SetActive(false);
        //         }
        //     }
        // }
    }
}
