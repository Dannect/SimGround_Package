using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Quiz
{
    public class Feedback : MonoBehaviour
    {
        [SerializeField] private TMP_Text feedbackText;
        [SerializeField] private Image backgroundImage;
        [SerializeField] private Sprite[] backgroundSprite;
        [SerializeField] private Image IncorrectImage;
        [SerializeField] private Sprite[] IncorrectSprite;

        public void SetFeedback(string feedback, bool isCorrect)
        {
            feedbackText.text = feedback;
            backgroundImage.sprite = isCorrect ? backgroundSprite[0] : backgroundSprite[1];
            IncorrectImage.sprite = isCorrect ? IncorrectSprite[0] : IncorrectSprite[1];
        }
    }
}
