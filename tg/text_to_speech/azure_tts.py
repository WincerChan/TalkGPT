import edge_tts
from pydub import AudioSegment
from typing import List
from pydub.playback import play
import io
import threading
import asyncio
import queue
from time import time
from typing import Union
from tg.config import DevConfig

LANG = DevConfig.AZURE_VOICE_LANG
q = queue.Queue()


def forever_run(queue):
    while True:
        sentence, last = queue.get()
        play_audio(sentence, last=last)


def play_audio(audio_data: bytes, file_format="mp3", last=False) -> None:
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
    if last:
        DevConfig.REPLYING = False


async def forever_consume_queue(queue, play_queue):
    while True:
        comm_stream, last = queue.get()
        sentence_bytes: List[bytes] = []
        t = time()
        async for msg in comm_stream:
            match msg["type"]:
                case "audio":
                    if data := msg["data"]:
                        sentence_bytes.append(data)
                case _:
                    pass
        if len(sentence_bytes) > 10:
            play_queue.put((b"".join(sentence_bytes[1:-5]), last))
        else:
            play_queue.put((b"".join(sentence_bytes), last))


def forever_consume(q, play_q):
    asyncio.run(forever_consume_queue(q, play_q))


def speak_text(text: str, last=False):
    communicate = edge_tts.Communicate(text, LANG)
    q.put((communicate.stream(), last))


play_queue = queue.Queue()
tts_worker = threading.Thread(target=forever_consume, args=(q, play_queue))
tts_worker.daemon = True
tts_worker.start()


player_worker = threading.Thread(target=forever_run, args=(play_queue,))
player_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question:")
        speak_text(text)
