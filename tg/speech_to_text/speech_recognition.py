import logging
from itertools import count

import speech_recognition as sr
from dotenv import set_key

from tg.config import DevConfig

match DevConfig.STT_CHOICE:
    case "WHISPER":
        from .whisper_stt import recognition
    case _:
        from .google_stt import recognition


logger = logging.getLogger("stt")

r = sr.Recognizer()


def devices_changed():
    audio = sr.Microphone.get_pyaudio().PyAudio()
    now_count = audio.get_device_count()
    before_count = DevConfig.MIC_DEVICE_COUNT
    set_key(".env", "MIC_DEVICE_COUNT", f"{now_count}")
    return f"{now_count}" != before_count


def list_input_device():
    audio = sr.Microphone.get_pyaudio().PyAudio()
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info.get("maxInputChannels") > 0:
            yield device_info.get("name"), i


def select_microphone():
    if devices_changed():
        DevConfig.MIC_DEVICE_INDEX = None
    if DevConfig.MIC_DEVICE_INDEX is None:
        print("Your device has many microphones: ")
    device_ids = []
    for idx, (mic_name, rel_idx) in enumerate(list_input_device()):
        device_ids.append(rel_idx)
        if DevConfig.MIC_DEVICE_INDEX is None:
            print(f"\t {idx+1}. {mic_name}")
            continue
        if DevConfig.MIC_DEVICE_INDEX == f"{rel_idx}":
            print(f"Your choose {mic_name} as microphone.")
            device_index = rel_idx
    if DevConfig.MIC_DEVICE_INDEX is None:
        device_index = device_ids[int(input("Please choose one: ")) - 1]
        set_key(".env", "MIC_DEVICE_INDEX", f"{device_index}")
    # log device index
    return sr.Microphone(device_index=device_index)


def listen(mic):
    while True:
        print("\nRecording, please speak...")
        try:
            with mic as source:
                audio = r.listen(source, phrase_time_limit=DevConfig.MAX_WAIT_SECONDS)
        except sr.WaitTimeoutError:
            input(
                f"No sound detected within {DevConfig.MAX_WAIT_SECONDS} seconds, enter hibernation mode, press [Enter] to wake up."
            )
            continue
        else:
            print("Recording finished, processing...")
        if DevConfig.REPLYING:
            continue
        yield recognition(audio)
