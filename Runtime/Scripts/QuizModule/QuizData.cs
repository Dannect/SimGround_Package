using System;
using System.Collections.Generic;

namespace Quiz
{
    // [Serializable]
    // public class RootResponse
    // {
    //     public bool success;
    //     public string message;
    //     public string code;
    //     public Data data;
    // }

    [Serializable]
    public class QuizData
    {
        public int id;
        public int accessCode;
        public bool isActive;
        public string expireDatetime;
        public CourseContent courseContent;
    }

    [Serializable]
    public class CourseContent
    {
        public int id;
        public string name;
        public string backgroundImage;
        public List<CourseContentDetail> courseContentDetails;
    }

    [Serializable]
    public class CourseContentDetail
    {
        public int id;
        public int step;
        public string activityStage;
        public string unityUrls;
        public List<MultipleChoiceQuizData> multipleChoiceQuizzes;
        public List<OxChoiceQuizData> oxChoiceQuizzes;
        public List<ShortQuizData> shortQuizzes;
        public List<ClassificationQuizData> classificationQuizzes;
        public List<BlankQuizData> blankQuizzes;
        public string equipments;
    }

    [Serializable]
    public class MultipleChoiceQuizData
    {
        public int id;
        public string uuid;
        public int quizStep;
        public string question;
        public string explanation;
        public string firstOption;
        public string firstFeedback;
        public string secondOption;
        public string secondFeedback;
        public string thirdOption;
        public string thirdFeedback;
        public string fourthOption;
        public string fourthFeedback;
        public int correctOption;
    }

    [Serializable]
    public class OxChoiceQuizData
    {
        public int id;
        public string uuid;
        public int quizStep;
        public string question;
        public string explanation;
        public string firstOption;
        public string firstFeedback;
        public string secondOption;
        public string secondFeedback;
        public int correctOption;
    }

    [Serializable]
    public class ShortQuizData
    {
        public int id;
        public string uuid;
        public int quizStep;
        public string question;
        public string rubric;
        public string feedbackSample;
    }

    [Serializable]
    public class ClassificationQuizData
    {
        public int id;
        public string uuid;
        public int quizStep;
        public string correctFeedback;
        public string incorrectFeedback;
        public List<Section> sections;
        public List<SectionItem> sectionItems;
    }

    [Serializable]
    public class Section
    {
        public int id;
        public string question;
        public List<int> correctItemIds;
    }

    [Serializable]
    public class SectionItem
    {
        public int id;
        public string name;
        public string imageUrl;
    }

    [Serializable]
    public class BlankQuizData
    {
        public int id;
        public string uuid;
        public int quizStep;
        public string question;
        public string explanation;
        public string firstOption;
        public string firstFeedback;
        public string secondOption;
        public string secondFeedback;
        public string thirdOption;
        public string thirdFeedback;
        public int correctOption;
    }

    [Serializable]
    public class QuizResponse
    {
        public bool success;
        public string message;
        public string code;
        public QuizResponseData data;
    }

    [Serializable]
    public class QuizResponseData
    {
        public string feedback;
        public bool isCorrect;
        public bool success;
    }

    [Serializable]
    public class QuizAnswerData
    {
        public string quizType;
        public int quizId;
        public string studentAnswer;
        public int timeTaken;
    }

    [Serializable]
    public class QuizSubmitData
    {
        public string type;
        public QuizAnswerData data;
    }
}
