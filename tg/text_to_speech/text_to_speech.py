import edge_tts
import time
from pydub import AudioSegment
from typing import List
from pydub.playback import play
import io
import asyncio
from typing import Union
from .utils import ThreadEventLoop

VOICE = "zh-CN-YunxiNeural"
t = ThreadEventLoop()
VOICE_QUEUES = asyncio.Queue(loop=t.loop)


def play_audio(audio_data: bytes, file_format="mp3") -> None:
    """
    Play audio data.

    Args:
        audio_data (bytes): Audio data to play.
        file_format (str): Audio file format, e.g., "mp3", "wav".
    """
    # Create audio segment from audio data
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format=file_format)

    # Play audio
    play(audio_segment)


async def forever_consume_queue():
    print("fjkkjdkjx")
    while True:
        print("fkfld")
        comm_stream = await VOICE_QUEUES.get()
        print("got one item")
        sentence_bytes: List[bytes] = []
        async for msg in comm_stream:
            if len(sentence_bytes) >= 10:
                play_audio(b"".join(sentence_bytes))
                sentence_bytes.clear()
            if msg["type"] == "audio":
                sentence_bytes.append(msg["data"])
            elif msg["type"] == "WordBoundary":
                print("\n")
        play_audio(b"".join(sentence_bytes))


def speek_text(text: str):
    communicate = edge_tts.Communicate(text, VOICE)
    VOICE_QUEUES.put_nowait(communicate.stream())


asyncio.run_coroutine_threadsafe(forever_consume_queue(), t.loop)
