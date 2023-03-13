import re

delimiter_pattern = re.compile(r"(?<=[.!?\\,，。！])+")


def contains_delimiter(char):
    if not char:
        return False
    return delimiter_pattern.search(char) is not None
