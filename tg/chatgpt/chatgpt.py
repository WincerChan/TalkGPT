import openai
import asyncio
import time
from tg.config import DevConfig
from ..text_to_speech.text_to_speech import speek_text

openai.api_key = DevConfig.API_KEY


def speek_queue(words):
    t = time.time()
    speek_text("".join(words))
    print(time.time() - t)


def chat(text):
    messages = [
        {"role": "system", "content": "in concise language"},
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
        if len(sentences) > 10:
            speek_queue(sentences)
            sentences.clear()
        choice = word["choices"][0]
        content = choice.get("delta").get("content")
        if content is None:
            continue
        sentences.append(content)
    speek_queue(sentences)
