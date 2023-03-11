import openai
import tempfile
import logging

from io import BytesIO, BufferedReader

logger = logging.getLogger("whisper")


def recognition(audio_bytes):
    tmp_file = BytesIO(audio_bytes)
    tmp_file.name = "input.wav"
    tmp_file.seek(0)
    resp = openai.Audio.transcribe("whisper-1", tmp_file)
    return resp["text"]
