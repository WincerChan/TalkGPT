from gtts import gTTS
from pydub import AudioSegment
from typing import List
from pydub.playback import play
import io
import threading
import queue
from tg.config import DevConfig

LANG = DevConfig.GOOGLE_VOICE_LANG
q = queue.Queue()


def forever_run(queue):
    while True:
        sentence: bytes = queue.get()
        play_audio(sentence)


def play_audio(audio_data: bytes, file_format="mp3") -> None:
    """
    Play audio data.

    Args:
        audio_data (bytes): Audio data to play.
        file_format (str): Audio file format, e.g., "mp3", "wav".
    """
    # Create audio segment from audio data
    try:
        audio_segment = AudioSegment.from_file(
            io.BytesIO(audio_data), format=file_format
        )
    except Exception as e:
        pass
        # print(audio_data)
    else:
        # Play audio
        play(audio_segment)


def forever_consume_queue(queue, play_queue):
    while True:
        comm_stream = queue.get()
        for msg in comm_stream:
            start_index = int(len(msg) // 120)
            end_index = int(len(msg) // 20)
            play_queue.put(msg[start_index:-end_index])


def speak_text(text: str):
    if len(text) == 1:
        return
    try:
        g_comm = gTTS(text, lang=LANG)
    except Exception as e:
        print(e)
    else:
        q.put(g_comm.stream())


play_queue = queue.Queue()
tts_worker = threading.Thread(target=forever_consume_queue, args=(q, play_queue))
tts_worker.daemon = True
tts_worker.start()


player_worker = threading.Thread(target=forever_run, args=(play_queue,))
player_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question:")
        speak_text(text)
