using UnityEngine;

namespace Quiz
{
    public interface IQuiz
    {
        public void BuildQuiz();
        void SetQuizData(object quizData);
        public void SubmitQuiz();
        public void SetSolvedQuizData(object quizData);
        public void ResponseFeedback(string responseData);
        public void ShowTeacherView();
    }
}
