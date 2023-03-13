from pocketsphinx import LiveSpeech


def listen():
    for phrase in LiveSpeech():
        yield phrase
