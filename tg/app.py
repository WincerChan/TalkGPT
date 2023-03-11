from tg.chatgpt import ask
import logging
import time

import speech_recognition as sr
from tg.speech_to_text import listen, select_microphone
from tg.config import DevConfig

logger = logging.getLogger("")


def raw_listen():
    logger.warning("Okkk ")
    for sentence in listen():
        for i, s in enumerate(choices := sentence.best()):
            print(f"{i}: {s[0]}")
        real_sentence = int(
            input("Your Voice maybe has many choinces, Please Input Number: ")
        )
        if real_sentence == -1:
            continue
        ask(choices[real_sentence][0])


def gg_listen():
    r = sr.Recognizer()
    logger.warning("Your device has many microphtos: ")
    for idx, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if DevConfig.DEVICE_NAME is None:
            print(f"{idx+1}. {mic_name}")
            continue

        if DevConfig.DEVICE_NAME == mic_name:
            print(f"You choose {DevConfig.DEVICE_NAME} as microphone.")
            device_index = idx
            break
    if DevConfig.DEVICE_NAME is None:
        device_index = int(input("Please choose one: ")) - 1
    mic = sr.Microphone(device_index=device_index)
    while True:
        with mic as source:
            audio = r.listen(source)
        if DevConfig.REPLYING:
            continue
        try:
            ret = r.recognize_google(audio, language="zh-CN", verbose=False)
        except sr.UnknownValueError:
            input(
                "No sound is detected, enter hibernation mode, press the Enter key to wake up"
            )
            continue
        ask(ret)


def run():
    mic = select_microphone()
    for x in listen(mic):
        if not x:
            continue
        print(f"Ask: {x}")
        ask(x)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        exit(0)
