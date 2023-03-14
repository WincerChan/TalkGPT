import speech_recognition as sr
from tg.config import DevConfig

r = sr.Recognizer()


def recognition(audio):
    try:
        ret = r.recognize_google(audio, language=DevConfig.GOOGLE_INPUT_LANG)
    except sr.UnknownValueError:
        input(
            "No sound is detected, enter hibernation mode, press the Enter key to wake up"
        )
        return
    return ret
