import asyncio

from tg.chatgpt import ask
from tg.speech_to_text import listen, select_microphone


def run():
    mic = select_microphone()
    for x in listen(mic):
        if not x:
            continue
        print(f"\nAsk: {x}")
        asyncio.run(ask(x))


if __name__ == "__main__":
    try:
        run()
    # Ctrl+C to exit
    except KeyboardInterrupt:
        exit(0)
