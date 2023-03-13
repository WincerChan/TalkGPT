from subprocess import call
import threading
import sys, os
import queue
from tg.config import DevConfig

msg_queue = queue.Queue()

currenct_pwd = os.getcwd()
current_file_path = os.path.abspath(__file__)
currenct_dir = os.path.dirname(current_file_path)


def forever_consume_queue(queue):
    while True:
        text, last = queue.get()
        call([sys.executable, os.path.join(currenct_dir, "_pyttsx.py"), text])
        if last:
            DevConfig.REPLYING = False


def speak_text(text: str, last=False):
    msg_queue.put((text, last))


tts_worker = threading.Thread(target=forever_consume_queue, args=(msg_queue,))
tts_worker.daemon = True
tts_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question: ")
        speak_text(text)
