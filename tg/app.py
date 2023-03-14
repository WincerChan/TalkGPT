from tg.chatgpt import ask

from tg.speech_to_text import listen, select_microphone
from tg.config import DevConfig


def run():
    mic = select_microphone()
    for x in listen(mic):
        if not x:
            continue
        print(f"Ask: {x}")
        ask(x)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        exit(0)
