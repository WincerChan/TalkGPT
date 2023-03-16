from gtts import gTTS
from pydub import AudioSegment
from typing import List
from pydub.playback import play
import io
import logging
import threading
import queue
from tg.config import DevConfig

LANG = DevConfig.GOOGLE_VOICE_LANG
play_queue = queue.Queue()
logger = logging.getLogger("google-tts")


def monitor_playback_queue(queue):
    while True:
        audio_data = queue.get()
        play_audio_segment(audio_data)


def play_audio_segment(audio_data: bytes, file_format="mp3") -> None:
    if not audio_data:
        DevConfig.REPLYING = False
        return
    try:
        audio_segment = AudioSegment.from_file(
            io.BytesIO(audio_data), format=file_format
        )
    except Exception as e:
        logger.exception(e)
    else:
        play(audio_segment)


def process_audio_stream(stream):
    if not stream:
        play_queue.put(b"")
        return

    for msg in stream:
        # 去掉首尾空白片段
        start_index = int(len(msg) // 120)
        end_index = int(len(msg) // 20)
        play_queue.put(msg[start_index:-end_index])


def speak_text(text: str):
    end_marker = "<END>"
    if text == end_marker or len(text) < 1:
        process_audio_stream(None)
        return
    try:
        g_comm = gTTS(text, lang=LANG)
    except Exception as e:
        logger.exception(e)
    else:
        process_audio_stream(g_comm.stream())


player_worker = threading.Thread(target=monitor_playback_queue, args=(play_queue,))
player_worker.daemon = True
player_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question:")
        speak_text(text)
