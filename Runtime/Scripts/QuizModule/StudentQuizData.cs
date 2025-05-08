using System;
using System.Collections.Generic;

namespace Quiz
{
    // [Serializable]
    // public class StudentQuizResponse
    // {
    //     public bool success;
    //     public string message;
    //     public string code;
    //     public StudentQuizData data;
    // }

    [Serializable]
    public class StudentQuizData
    {
        public int id;
        public int userId;
        public string userName;
        public int grade;
        public int semester;
        public string chapterGroupName;
        public int chapterGroupNumber;
        public string createdAt;
        public string courseContentName;
        public string courseContentPreviewImage;
        public List<QuizByStageAndStep> quizzesByStageAndStep;
        public string aiFeedback;
    }

    [Serializable]
    public class QuizByStageAndStep
    {
        public string activityStage;
        public int step;
        public MultipleChoiceQuiz multipleChoiceQuiz;
        public OxQuiz oxQuiz;
        public ShortQuiz shortQuiz;
        public ClassificationQuiz classificationQuiz;
        public BlankQuiz blankQuiz;
        public string imageQuiz;
    }

    [Serializable]
    public class MultipleChoiceQuiz
    {
        public int studentId;
        public int step;
        public string question;
        public string firstOption;
        public string secondOption;
        public string thirdOption;
        public string fourthOption;
        public string firstFeedback;
        public string secondFeedback;
        public string thirdFeedback;
        public string fourthFeedback;
        public string activityStage;
        public int id;
        public string studentAnswer;
        public bool isCorrect;
        public string submittedAt;
        public int timeTaken;
    }

    [Serializable]
    public class OxQuiz
    {
        public int studentId;
        public int step;
        public string question;
        public string firstOption;
        public string secondOption;
        public string firstFeedback;
        public string secondFeedback;
        public string activityStage;
        public int id;
        public string studentAnswer;
        public bool isCorrect;
        public string correctAnswer;
        public string submittedAt;
        public int timeTaken;
    }

    [Serializable]
    public class ShortQuiz
    {
        public int studentId;
        public int step;
        public string question;
        public string correctAnswer;
        public string activityStage;
        public int? id;
        public string studentAnswer;
        public bool isCorrect;
        public string feedback;
        public string submittedAt;
        public int timeTaken;
        public string feedbackSample;
    }

    [Serializable]
    public class ClassificationQuiz
    {
        public int studentId;
        public int step;
        public string question;
        public List<string> categories;
        public List<ClassificationItem> items;
        public string activityStage;
        public Dictionary<string, List<ClassificationItem>> correctAnswer;
        public int id;
        public Dictionary<string, List<ClassificationItem>> studentAnswer;
        public bool isCorrect;
        public string correctFeedback;
        public string inCorrectFeedback;
        public string submittedAt;
        public int timeTaken;
    }

    [Serializable]
    public class ClassificationItem
    {
        public string name;
        public string imageUrl;
    }

    [Serializable]
    public class BlankQuiz
    {
        public int studentId;
        public int step;
        public string question;
        public string firstOption;
        public string secondOption;
        public string thirdOption;
        public string firstFeedback;
        public string secondFeedback;
        public string thirdFeedback;
        public string activityStage;
        public int id;
        public string studentAnswer;
        public bool isCorrect;
        public int correctAnswer;
        public string submittedAt;
        public int timeTaken;
    }
}

