import unittest
from EmotionDetection import emotion_detector

class TestEmotionDetector(unittest.TestCase):
    
    def test_joy_emotion(self): 
        result = emotion_detector('I am glad this happened.')
        self.assertIn('joy', result, "The emotion 'joy' should be detected.")

    def test_anger_emotion(self):
        result = emotion_detector('I am really mad about this.')
        self.assertIn('anger', result, "The emotion 'anger' should be detected.")

    def test_disgust_emotion(self):
        result = emotion_detector('I feel disgusted just hearing about this.')
        self.assertIn('disgust', result, "The emotion 'disgust' should be detected.")

    def test_sadness_emotion(self):
        result = emotion_detector('I am so sad about this.')
        self.assertIn('sadness', result, "The emotion 'sadness' should be detected.")

    def test_fear_emotion(self):
        result = emotion_detector('I am really afraid that this will happen.')
        self.assertIn('fear', result, "The emotion 'fear' should be detected.")

if __name__ == '__main__':
    unittest.main()
