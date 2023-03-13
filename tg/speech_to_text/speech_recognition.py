from pocketsphinx import LiveSpeech
from tg.config import DevConfig
import logging

logger = logging.getLogger("stt")


def listen():
    for phrase in LiveSpeech():
        logger.warning(f"{phrase} {DevConfig.REPLYING}")
        if DevConfig.REPLYING:
            continue
        yield phrase
