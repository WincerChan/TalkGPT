import edge_tts
from pydub import AudioSegment
from typing import List
from pydub.playback import play
import io
import threading
import asyncio
import queue
import logging
from tg.config import DevConfig

LANG = DevConfig.AZURE_VOICE_LANG
logger = logging.getLogger("azure-ttl")
playback_queue = queue.Queue()


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


async def process_audio_stream(stream, is_last):
    if not stream:
        playback_queue.put(b"")
        return

    audio_bytes: List[bytes] = []

    async for msg in stream:
        if msg["type"] == "audio" and (data := msg["data"]):
            audio_bytes.append(data)

    if len(audio_bytes) > 10:
        audio_bytes = audio_bytes[1:-5]

    playback_queue.put(b"".join(audio_bytes))


def synthesize_speech_from_text(text: str):
    end_marker = "<END>"
    if text == end_marker:
        stream = None
    else:
        stream = edge_tts.Communicate(text, LANG).stream()

    asyncio.run(process_audio_stream(stream, False))


player_thread = threading.Thread(target=monitor_playback_queue, args=(playback_queue,))
player_thread.daemon = True
player_thread.start()

if __name__ == "__main__":
    while True:
        text = input("Question:")
        synthesize_speech_from_text(text)
