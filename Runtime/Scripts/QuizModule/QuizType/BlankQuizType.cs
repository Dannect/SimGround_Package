using UnityEngine;
using UnityEngine.UI;
using TMPro;
namespace Quiz
{
    public class BlankQuizType : QuizBase, IQuiz
    {
        [SerializeField] private TMP_Text firstQuestionText;
        [SerializeField] private TMP_Text lastQuestionText;
        [SerializeField] private GameObject answerSlotObject;
        [SerializeField] private TMP_Text answerSlot;
        [SerializeField] private TMP_Text firstOptionText;
        [SerializeField] private TMP_Text secondOptionText;
        [SerializeField] private TMP_Text thirdOptionText;
        [SerializeField] private Button[] threePanelButtons;
        [SerializeField] private Image[] threeRadioImages;
        [SerializeField] private Sprite[] panelSprites;
        [SerializeField] private Sprite[] radioSprites;
        private int answer = -1;
        private int correctAnswer = -1;
        private BlankQuizData quizData;
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
            this.quizData = (BlankQuizData)quizData;
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
            firstQuestionText.text = first;
            lastQuestionText.text = last;

            // AnswerSlot, LastText 오브젝트 활성화
            answerSlotObject.SetActive(true);
            lastQuestionText.gameObject.SetActive(true);

            firstOptionText.text = this.quizData.firstOption;
            secondOptionText.text = this.quizData.secondOption;
            thirdOptionText.text = this.quizData.thirdOption;

            correctAnswer = this.quizData.correctOption;
        }
        public void SubmitQuiz()
        {
            submitButton.interactable = false;
            isCheckTime = false;
            QuizAnswerData submitData = new QuizAnswerData
            {
                quizType = "BLANK",
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
            if (quizData is BlankQuiz data)
            {
                if (data.studentAnswer == null) return;

                answer = int.Parse(data.studentAnswer);
                On3OptionsButtonClick(answer - 1);
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

            bool isCorrect = answer == correctAnswer ? true : false;

            feedback.SetFeedback(feedbackText, isCorrect);
            feedback.gameObject.SetActive(true);
            submitObject.SetActive(false);
        }

        public void ShowTeacherView()
        {
            answer = correctAnswer;
            On3OptionsButtonClick(correctAnswer - 1);
            ResponseFeedback("");
        }
        public void On3OptionsButtonClick(int index)
        {
            if (answer == -1)
            {
                submitButton.interactable = true;
            }
            answer = index + 1;

            if (index == 0)
            {
                answerSlot.text = quizData.firstOption;
            }
            else if (index == 1)
            {
                answerSlot.text = quizData.secondOption;
            }
            else if (index == 2)
            {
                answerSlot.text = quizData.thirdOption;
            }
            // 모든 라디오 버튼 초기화
            for (int i = 0; i < 3; i++)
            {
                threeRadioImages[i].sprite = radioSprites[0];

                // 패널 버튼 이미지 설정
                if (i < threePanelButtons.Length)
                {
                    threePanelButtons[i].image.sprite = panelSprites[i + 3]; // 기본 상태는 index + 4
                }
            }

            // 선택한 라디오 버튼만 활성화
            Debug.Log("On3OptionsButtonClick: " + index);
            threeRadioImages[index].sprite = radioSprites[1];

            // 선택한 패널 버튼 이미지 변경
            if (index < threePanelButtons.Length)
            {
                threePanelButtons[index].image.sprite = panelSprites[index]; // 선택한 버튼은 index
            }
        }

        private void ResetImages()
        {
            for (int i = 0; i < 3; i++)
            {
                threeRadioImages[i].sprite = radioSprites[0];
                threePanelButtons[i].image.sprite = panelSprites[i];
            }
        }
    }
}
