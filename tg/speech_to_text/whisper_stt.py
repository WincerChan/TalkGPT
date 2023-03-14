import speech_recognition as sr
from tg.config import DevConfig
import logging

r = sr.Recognizer()

logger = logging.getLogger("whisper")


def recognition(audio):
    try:
        ret = r.recognize_whisper_api(audio, api_key=DevConfig.API_KEY)
    except sr.UnknownValueError:
        input(
            "No sound is detected, enter hibernation mode, press the Enter key to wake up"
        )
        return
    return ret
