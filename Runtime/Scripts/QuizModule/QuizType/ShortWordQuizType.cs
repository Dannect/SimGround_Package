using UnityEngine;
using System;
using TMPro;
using System.Collections;
using UnityEngine.Networking;

namespace Quiz
{
    public class ShortWordQuizType : QuizBase, IQuiz
    {
        [SerializeField] private TMP_Text firstText;
        [SerializeField] private TMP_Text lastText;
        [SerializeField] private GameObject answerSlotObject;
        [SerializeField] private TMP_Text answerSlot;
        [SerializeField] private TMP_InputField answerInputField;

        private ShortQuizData quizData;
        public void BuildQuiz()
        {
            InitQuizUI();
            answerInputField.text = "";
            answerInputField.onValueChanged.RemoveAllListeners();
            answerInputField.onValueChanged.AddListener((value) =>
            {
                Debug.Log("value: " + value);
                if (value.Length > 0)
                {
                    Debug.Log("submitButton.interactable: " + submitButton.interactable);
                    submitButton.interactable = true;
                }
                else
                {
                    Debug.Log("submitButton.interactable: " + submitButton.interactable);
                    submitButton.interactable = false;
                }
            });
            submitButton.onClick.RemoveAllListeners();
            submitButton.onClick.AddListener(SubmitQuiz);
            isCheckTime = true;
        }

        public void SetQuizData(object quizData)
        {
            this.quizData = (ShortQuizData)quizData;
            id = this.quizData.id;
            uuid = this.quizData.uuid;
            quizStep = this.quizData.quizStep;
            question = this.quizData.question;

            // 문제 텍스트를 {{}} 기준으로 분리
            string first = question;
            string last = "";
            int idx = question.IndexOf("{{}}");
            if (idx >= 0)
            {
                first = question.Substring(0, idx);
                last = question.Substring(idx + 4); // 4는 {{}} 길이
            }

            // 모든 자식(자식의 자식 포함)에서 FirstText, LastText, AnswerSlot을 찾는다
            firstText.text = first;
            lastText.text = last;

            // AnswerSlot, LastText 오브젝트 활성화
            answerSlotObject.SetActive(true);
            lastText.gameObject.SetActive(true);

        }
        public void SetSolvedQuizData(object quizData)
        {
            if (quizData is ShortQuiz data)
            {
                if (data.studentAnswer == null) return;
                Debug.Log("data.studentAnswer: " + data.studentAnswer);
                feedback.gameObject.SetActive(true);
                nextObject.SetActive(true);
                submitObject.SetActive(false);
                feedback.SetFeedback(data.feedback, data.isCorrect);
                answerSlot.text = data.studentAnswer;
                gameObject.SetActive(false);
            }
        }
        public void ShowTeacherView()
        {
            ActiveFeedbackUI(quizData.feedbackSample, true);
            feedback.gameObject.SetActive(true);
            submitObject.SetActive(false);
            gameObject.SetActive(false);
        }
        public void SubmitQuiz()
        {
            //제출 webRequest 호출
            if (answerInputField.text.Length <= 0) return;
            Debug.Log("Submit ShortWordQuiz");
            submitButton.interactable = false;
            isCheckTime = false;
            answerSlot.text = answerInputField.text;
            QuizAnswerData submitData = new QuizAnswerData
            {
                quizType = "SHORT_ANSWER",
                quizId = id,
                studentAnswer = answerInputField.text,
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
            Managers.Quiz.currentQuiz = this;
        }

        public void ResponseFeedback(string responseData)
        {
            QuizResponseData response = JsonUtility.FromJson<QuizResponseData>(responseData);
            Debug.Log("ResponseFeedback: " + response.feedback);
            ActiveFeedbackUI(response.feedback, response.isCorrect);
            feedback.gameObject.SetActive(true);
            nextObject.SetActive(true);
            submitObject.SetActive(false);
            gameObject.SetActive(false);
        }
    }
}

