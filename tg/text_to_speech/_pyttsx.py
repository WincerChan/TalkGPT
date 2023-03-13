import sys
import pyttsx3


engine = pyttsx3.init()


def say(s):
    engine.say(s)
    engine.runAndWait()  # blocks


if __name__ == "__main__":
    if len(sys.argv) > 1:
        say(str(sys.argv[1]))
    else:
        print("not enough")
