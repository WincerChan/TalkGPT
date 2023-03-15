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


def _words_to_sentence(words):
    sentence = "".join(words).replace("\n\n", "\n")
    print(sentence, end="", flush=True)
    return sentence


def words_to_speek(words):
    sentence = _words_to_sentence(words)
    speak_text(sentence)
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
    reply, words = [], []
    for word in stream:
        best_choice = word["choices"][0]

        content: str
        if content := best_choice["delta"].get("content"):
            words.append(content.replace("\n", "", 1))

        reply_finished = best_choice["finish_reason"] == "stop"

        is_complete_sentence = contains_delimiter(content) and len(words) > 10

        if is_complete_sentence or reply_finished:
            reply.append(words_to_speek(words))
            words.clear()
    else:
        reply.append(words_to_speek(words))

    speak_text("<END>")

    return "".join(reply)


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
    print("Reply: ", end="")
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
