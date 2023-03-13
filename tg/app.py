from tg.chatgpt import ask
import logging

from tg.speech_to_text import listen

logger = logging.getLogger("")


def run():
    for sentence in listen():
        logger.debug(f"User Input: {sentence}")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        exit(0)
