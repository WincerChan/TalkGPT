import asyncio
import io
import logging
from typing import List

from pydub import AudioSegment
from pydub.playback import play

from tg.config import DevConfig

logger = logging.getLogger("base-tts")


class BaseSpeech:
    def __init__(self) -> None:
        self.audio_queue = asyncio.Queue()
        self.consumer_task = asyncio.create_task(self.audio_consumer())
        self.play_tasks = []

    async def wait_for_play(self):
        await asyncio.gather(*self.play_tasks)
        await self.do_speak(len(self.play_tasks), "<END>")
        await self.consumer_task

    async def audio_consumer(self):
        expected_idx = 0
        while True:
            idx, audio_data = await self.audio_queue.get()
            if not audio_data and self.audio_queue.qsize() == 0:
                DevConfig.REPLYING = False
                break
            if expected_idx != idx:
                # 下标不对，放回
                await asyncio.sleep(0.1)
                await self.audio_queue.put((idx, audio_data))
                continue
            try:
                audio_segment = AudioSegment.from_file(
                    io.BytesIO(audio_data), format="mp3"
                )
            except Exception as e:
                logger.exception(e)
            else:
                await asyncio.to_thread(play, audio_segment)
                expected_idx += 1

    def get_stream(self, text):
        raise NotImplementedError

    async def do_speak(self, idx, text):
        end_marker = "<END>"
        if text == end_marker:
            stream = None
        else:
            stream = self.get_stream(text)
        await self.process_audio_stream(idx, stream)

    async def process_audio_stream(self, idx, stream):
        raise NotImplementedError

    def speak_text(self, idx, text):
        if not text:
            return
        task = asyncio.create_task(self.do_speak(idx, text))
        self.play_tasks.append(task)
