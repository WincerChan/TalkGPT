import asyncio
import io
import logging
import queue

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from tg.config import DevConfig
from tg.text_to_speech.base_tts import BaseSpeech

LANG = DevConfig.GOOGLE_VOICE_LANG
play_queue = queue.Queue()
logger = logging.getLogger("google-tts")


class Speech(BaseSpeech):
    async def _build_async_stream(self, stream):
        for msg in stream:
            yield await asyncio.to_thread(lambda: msg)

    async def process_audio_stream(self, idx, stream):
        if not stream:
            await self.audio_queue.put((idx, None))
            return

        async for msg in self._build_async_stream(stream):
            # 去掉首尾空白片段
            start_index = int(len(msg) // 120)
            end_index = int(len(msg) // 20)
            await self.audio_queue.put((idx, msg[start_index:]))

    def get_stream(self, text):
        try:
            g_comm = gTTS(text, lang=LANG)
        except Exception as e:
            logger.exception(e)
        else:
            return g_comm.stream()


async def te():
    sp = Speech()
    sp.speak_text(0, "二")
    sp.speak_text(2, "一二三四五六七八九十")
    sp.speak_text(1, "三四五")
    sp.speak_text(3, "四")
    await sp.wait_for_play()


if __name__ == "__main__":
    asyncio.run(te())
