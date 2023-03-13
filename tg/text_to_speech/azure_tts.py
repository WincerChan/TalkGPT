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
play_queue = queue.Queue()


def wait_for_play(queue):
    while True:
        sentence, last = queue.get()
        play_audio(sentence, last=last)


def play_audio(audio_data: bytes, file_format="mp3", last=False) -> None:
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


async def handle_stream(stream, last):
    if not stream:
        play_queue.put((b"", last))
        return
    sentence_bytes: List[bytes] = []
    async for msg in stream:
        match msg["type"]:
            case "audio":
                if data := msg["data"]:
                    sentence_bytes.append(data)
            case _:
                pass
    # 去掉 tts 返回的录音片段里首尾包含的空白片段
    if (ed := len(sentence_bytes)) > 10:
        ed = -5
    play_queue.put((b"".join(sentence_bytes[1:ed]), last))


def speak_text(text: str, last=False):
    match (text, last):
        case ("", True):
            stream = None
        case _:
            stream = edge_tts.Communicate(text, LANG).stream()
    asyncio.run(handle_stream(stream, last))


player_worker = threading.Thread(target=wait_for_play, args=(play_queue,))
player_worker.daemon = True
player_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question:")
        speak_text(text)
