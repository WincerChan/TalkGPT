from pocketsphinx import LiveSpeech
from tg.config import DevConfig
import speech_recognition as sr
import logging
from tg.config import DevConfig
from .whisper_stt import recognition as whiper_reco
from .google_stt import recognition as google_reco


logger = logging.getLogger("stt")

r = sr.Recognizer()


def select_microphone():
    if DevConfig.DEVICE_NAME is None:
        print("Your device has many microphones: ")
    for idx, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if DevConfig.DEVICE_NAME is None:
            print(f"\t {idx+1}. {mic_name}")
            continue
        if DevConfig.DEVICE_NAME == mic_name:
            print(f"Your choose {DevConfig.DEVICE_NAME} as microphone.")
            device_index = idx
    if DevConfig.DEVICE_NAME is None:
        device_index = int(input("Please choose one: ")) - 1
    return sr.Microphone(device_index=device_index)


def listen(mic):
    while True:
        print("Listening...")
        with mic as source:
            audio = r.listen(source)
        if DevConfig.REPLYING:
            continue
        match DevConfig.STT_CHOICE:
            case "WHISPER":
                yield whiper_reco(audio.get_wav_data())
            case _:
                yield google_reco(audio, DevConfig.GOOGLE_INPUT_LANG)
