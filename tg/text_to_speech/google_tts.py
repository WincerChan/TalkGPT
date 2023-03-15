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


def wait_for_play(queue):
    while True:
        sentence, last = queue.get()
        play_audio(sentence, is_latis_last


def play_audio(audio_data: bytes, file_format="mp3", is_latFalse) -> None:
    # Create audio segment from audio data
    if audio_data:
        try:
            audio_segment = AudioSegment.from_file(
                io.BytesIO(audio_data), format=file_format
            )
        except Exception as e:
            logger.exception(e)
        else:
            play(audio_segment)
    DevConfig.REPLYING = not last


def handle_stream(stream, is_last:
    if not stream:
        play_queue.put((b"", is_last)
        return

    for msg in stream:
        # 去掉首尾空白片段
        start_index = int(len(msg) // 120)
        end_index = int(len(msg) // 20)
        play_queue.put((msg[start_index:-end_index], is_last)


def speak_text(text: str, is_latFalse):
    if len(text) < 1:
        handle_stream(None, is_last
        return
    try:
        g_comm = gTTS(text, lang=LANG)
    except Exception as e:
        logger.exception(e)
    else:
        handle_stream(g_comm.stream(), is_last


player_worker = threading.Thread(target=wait_for_play, args=(play_queue,))
player_worker.daemon = True
player_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question:")
        speak_text(text)
