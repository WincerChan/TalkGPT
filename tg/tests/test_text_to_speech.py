import unittest
from tg.text_to_speech.text_to_speech import speak_text
from tg.text_to_speech.native_tts import speak_text as native_speak


# class TestSpeekText(unittest.TestCase):
#     def test_speek_text(self):
#         speak_text("你好")
#         speak_text("，我也好")


class TestNativeTTS(unittest.TestCase):
    def test_native_tts(self):
        native_speak("你好")


if __name__ == "__main__":
    unittest.main()
