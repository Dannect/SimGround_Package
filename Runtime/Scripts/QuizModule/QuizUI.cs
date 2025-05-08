using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Quiz
{
    public class QuizUI : MonoBehaviour
    {
        public Sprite[] panelSprites;
        public Sprite[] radioSprites;
        public Image[] radioImages;

        public Sprite[] oxSprites;

        public Image[] oxRadioImages;

        public bool isSelected = false;

        public int answer;
    }
}
