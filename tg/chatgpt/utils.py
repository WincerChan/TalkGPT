import re
from collections import deque

delimiter_pattern = re.compile(r"(?<=[.!?\\,，。！])+")


def contains_delimiter(char):
    if not char:
        return False
    return delimiter_pattern.search(char) is not None


class CircularConversation:
    def __init__(self, capacity):
        self._dq = deque(maxlen=capacity)

    def push_ask(self, item):
        conversation = (item, None)
        self._dq.append(conversation)

    def push_reply(self, item):
        (ask, _) = self._dq[-1]
        self._dq[-1] = (ask, item)

    def __iter__(self):
        for ask, reply in self._dq:
            if ask:
                yield ask
            if reply:
                yield reply

    @property
    def queue(self):
        return list(self._dq)
