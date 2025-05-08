using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Quiz
{
    public class MultipleChoiceQuizType : QuizBase, IQuiz
    {
        [SerializeField] private TMP_Text questionText;
        [SerializeField] private TMP_Text firstOptionText;
        [SerializeField] private TMP_Text secondOptionText;
        [SerializeField] private TMP_Text thirdOptionText;
        [SerializeField] private TMP_Text fourthOptionText;

        [SerializeField] private Sprite[] panelSprites;
        [SerializeField] private Sprite[] radioSprites;
        [SerializeField] private Image[] radioImages;
        [SerializeField] private Button[] fourPanelButtons;

        private int answer = -1;
        private int correctAnswer = -1;
        private MultipleChoiceQuizData quizData;
        public void BuildQuiz()
        {
            InitQuizUI();
            submitButton.onClick.RemoveAllListeners();
            submitButton.onClick.AddListener(SubmitQuiz);
            ResetImages();
            answer = -1;
            isCheckTime = true;
        }

        public void SetQuizData(object quizData)
        {
            this.quizData = (MultipleChoiceQuizData)quizData;
            id = this.quizData.id;
            uuid = this.quizData.uuid;
            quizStep = this.quizData.quizStep;
            question = this.quizData.question;

            questionText.text = this.quizData.question;
            firstOptionText.text = this.quizData.firstOption;
            secondOptionText.text = this.quizData.secondOption;
            thirdOptionText.text = this.quizData.thirdOption;
            fourthOptionText.text = this.quizData.fourthOption;

            correctAnswer = this.quizData.correctOption;
        }

        public void SubmitQuiz()
        {
            submitButton.interactable = false;
            isCheckTime = false;
            QuizAnswerData submitData = new QuizAnswerData
            {
                quizType = "MULTIPLE_CHOICE",
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
            if (quizData is MultipleChoiceQuiz data)
            {
                if (data.studentAnswer == null) return;

                answer = int.Parse(data.studentAnswer);
                On4OptionsButtonClick(answer - 1);
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
            else if (answer == 3)
                feedbackText = quizData.thirdFeedback;
            else if (answer == 4)
                feedbackText = quizData.fourthFeedback;

            bool isCorrect = answer == correctAnswer ? true : false;

            feedback.SetFeedback(feedbackText, isCorrect);
            feedback.gameObject.SetActive(true);

            submitObject.SetActive(false);
        }
        public void ShowTeacherView()
        {
            answer = correctAnswer;
            On4OptionsButtonClick(correctAnswer - 1);
            ResponseFeedback("");
        }
        public void On4OptionsButtonClick(int index)
        {
            if (answer == -1)
            {
                submitButton.interactable = true;
            }
            answer = index + 1;

            // 모든 라디오 버튼 초기화
            for (int i = 0; i < radioImages.Length; i++)
            {
                radioImages[i].sprite = radioSprites[0];

                // 패널 버튼 이미지 설정
                if (i < fourPanelButtons.Length)
                {
                    fourPanelButtons[i].image.sprite = panelSprites[i + 4]; // 기본 상태는 index + 4
                }
            }

            // 선택한 라디오 버튼만 활성화
            radioImages[index].sprite = radioSprites[1];

            // 선택한 패널 버튼 이미지 변경
            if (index < fourPanelButtons.Length)
            {
                fourPanelButtons[index].image.sprite = panelSprites[index]; // 선택한 버튼은 index
            }
        }

        private void ResetImages()
        {
            for (int i = 0; i < radioImages.Length; i++)
            {
                radioImages[i].sprite = radioSprites[0];
                fourPanelButtons[i].image.sprite = panelSprites[i];
            }
        }
    }
}
