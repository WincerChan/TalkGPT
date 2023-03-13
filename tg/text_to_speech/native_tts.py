from subprocess import call
import threading
import sys, os
import queue

msg_queue = queue.Queue()

currenct_pwd = os.getcwd()
current_file_path = os.path.abspath(__file__)
currenct_dir = os.path.dirname(current_file_path)


def forever_consume_queue(queue):
    while True:
        text = queue.get()
        call([sys.executable, os.path.join(currenct_dir, "_pyttsx.py"), text])


def speak_text(text: str):
    msg_queue.put(text)


tts_worker = threading.Thread(target=forever_consume_queue, args=(msg_queue,))
tts_worker.daemon = True
tts_worker.start()

if __name__ == "__main__":
    while True:
        text = input("Question: ")
        speak_text(text)
