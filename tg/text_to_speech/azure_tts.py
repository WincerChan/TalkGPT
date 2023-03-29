import asyncio
import logging
from typing import List

import edge_tts

from tg.config import DevConfig
from tg.text_to_speech.base_tts import BaseSpeech

LANG = DevConfig.AZURE_VOICE_LANG
logger = logging.getLogger("azure-ttl")


class Speech(BaseSpeech):
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

    def get_stream(self, text):
        return edge_tts.Communicate(text, LANG).stream()


async def te():
    sp = Speech()
    sp.speak_text(0, "二")
    sp.speak_text(2, "一二三四五六七八九十")
    sp.speak_text(1, "三四五")
    sp.speak_text(3, "四")
    await sp.wait_for_play()


if __name__ == "__main__":
    asyncio.run(te())
