using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Quiz
{
    public class QuizBase : MonoBehaviour
    {
        protected GameObject content;

        protected int id;
        protected string uuid;
        public int quizStep;
        protected string question;
        public Feedback feedback;
        public GameObject submitObject;
        protected Button submitButton;
        public GameObject nextObject;
        protected Button nextButton;

        protected float timeTaken = 0;
        protected bool isCheckTime = false;
        public void InitQuizUI()
        {
            submitButton = submitObject.GetComponentInChildren<Button>();
            nextButton = nextObject.GetComponentInChildren<Button>();
            nextButton.onClick.AddListener(Managers.Quiz.OpenNextQuiz);
            feedback.gameObject.SetActive(false);
            timeTaken = 0;
        }
        // 자식의 자식까지 모두 탐색해서 오브젝트를 찾는 함수
        public Transform FindDeepChild(Transform parent, string name)
        {
            foreach (Transform child in parent)
            {
                if (child.name == name)
                    return child;
                var result = FindDeepChild(child, name);
                if (result != null)
                    return result;
            }
            return null;
        }

        void Update()
        {
            if (isCheckTime)
            {
                timeTaken += Time.deltaTime;
            }
        }

        protected virtual void ActiveFeedbackUI(string feedbackText, bool isCorrect)
        {
            feedback.gameObject.SetActive(true);
            feedback.SetFeedback(feedbackText, isCorrect);
        }
    }
}
