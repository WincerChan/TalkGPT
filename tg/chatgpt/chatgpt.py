import logging
import openai
import asyncio
import time
from tg.config import DevConfig
from ..text_to_speech.text_to_speech import speak_text
from .utils import contains_delimiter, CircularConversation

openai.api_key = DevConfig.API_KEY
# one conversation = 1 ask + 1 reply
PREVIOUS_CONVERSATIONS = CircularConversation(DevConfig.PREVIOUS_MESSAGES_COUNT + 1)
logger = logging.getLogger("chatgpt")


def to_speak(words, last=False):
    sentence = "".join(words)

    print(sentence, end="", flush=True)
    speak_text(sentence, last=last)
    return sentence


def build_conversation_context(text):
    DevConfig.REPLYING = True
    messages = [
        {"role": "system", "content": DevConfig.SYSTEM_PROMPT},
    ]
    PREVIOUS_CONVERSATIONS.push_ask({"role": "user", "content": text})
    messages.extend(PREVIOUS_CONVERSATIONS)
    logger.debug(messages)
    return messages


def build_sentence_from_stream(stream) -> str:
    reply = ""
    words = []
    for word in stream:
        best_choice = word["choices"][0]
        content = best_choice.get("delta").get("content")
        if content is None:
            continue

        words.append(content)

        if contains_delimiter(content) and len(words) > 10:
            reply += to_speak(words)
            words.clear()

    reply += to_speak(words, last=True)
    return reply


def save_reply(raw_reply):
    reply = {"role": "assistant", "content": raw_reply}
    PREVIOUS_CONVERSATIONS.push_reply(reply)


def ask(text):
    DevConfig.REPLYING = True
    messages = build_conversation_context(text)
    stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        stream=True,
    )
    reply = build_sentence_from_stream(stream)
    # save reply
    if DevConfig.PREVIOUS_MESSAGES_SAVE_REPLY:
        save_reply(reply)

    # block when this conversation is not finished.
    while DevConfig.REPLYING:
        time.sleep(0.1)


if __name__ == "__main__":
    while True:
        text = input("Question: ")
        ask(text)
