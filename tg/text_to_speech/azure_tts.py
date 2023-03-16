import edge_tts
from pydub import AudioSegment
from typing import List
from pydub.playback import play
from concurrent.futures import ThreadPoolExecutor
import io
import time
import asyncio
import logging
from tg.config import DevConfig

LANG = DevConfig.AZURE_VOICE_LANG
logger = logging.getLogger("azure-ttl")



class Speech:


    def __init__(self) -> None:
        self.audio_queue = asyncio.Queue()
        self.consumer_task = asyncio.create_task(self.audio_consumer())
        self.play_tasks = []

    async def wait_for_play(self):
        await asyncio.gather(*self.play_tasks)
        await self.do_speak(len(self.play_tasks), "<END>")
        await self.consumer_task

    async def process_audio_stream(self, idx, stream):
        if not stream:
            await self.audio_queue.put((idx, None))
            return

        audio_bytes: List[bytes] = []

        async for msg in stream:
            if msg["type"] == "audio" and (data := msg["data"]):
                audio_bytes.append(data)
        await stream.aclose()
        if len(audio_bytes) > 10:
            audio_bytes = audio_bytes[1:-5]
        await self.audio_queue.put((idx, b"".join(audio_bytes)))


    async def audio_consumer(self):
        expected_idx = 0
        loop = asyncio.get_running_loop()
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
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
            except Exception as e:
                logger.exception(e)
            else:
                await asyncio.to_thread(play, audio_segment)
                # play(audio_segment)
                expected_idx += 1

    async def do_speak(self, idx, text):
        end_marker = "<END>"
        if text == end_marker:
            stream = None
        else:
            stream = edge_tts.Communicate(text, LANG).stream()
        await self.process_audio_stream(idx, stream)

    def speak_text(self, idx, text):
        if not text:
            return
        task = asyncio.create_task(self.do_speak(idx, text))
        self.play_tasks.append(task)


async def te():
    sp = Speech()
    sp.speak_text(0,"二")
    sp.speak_text(2, "一二三四五六七八九十")
    sp.speak_text(1, "三四五")
    sp.speak_text(3,"四")
    await sp.wait_for_play()

if __name__ == "__main__":
    asyncio.run(te())
