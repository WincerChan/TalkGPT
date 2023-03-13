import openai
import asyncio
import time
from tg.config import DevConfig
from ..text_to_speech.text_to_speech import speak_text
from .utils import contains_delimiter

openai.api_key = DevConfig.API_KEY


def to_speak(words, last=False):
    speak_text("".join(words), last=last)
    print("".join(words))


def ask(text):
    DevConfig.REPLYING = True
    messages = [
        {"role": "system", "content": "说话简洁"},
        {"role": "user", "content": text},
    ]
    stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        stream=True,
    )
    sentences = []
    for word in stream:
        choice = word["choices"][0]
        content = choice.get("delta").get("content")
        if contains_delimiter(content) and len(sentences) > 10:
            to_speak(sentences)
            sentences.clear()

        if content is None:
            continue
        sentences.append(content)
    to_speak(sentences, last=True)
    while True:
        time.sleep(0.1)
        if DevConfig.REPLYING is False:
            break


if __name__ == "__main__":
    while True:
        text = input("Question: ")
        ask(text)
