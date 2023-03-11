import speech_recognition as sr
from tg.config import DevConfig

r = sr.Recognizer()


def recognition(audio, lang="zh-CN"):
    try:
        ret = r.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        input(
            "No sound is detected, enter hibernation mode, press the Enter key to wake up"
        )
        return
    return ret
