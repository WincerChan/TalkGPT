from dotenv import load_dotenv as _load_env
import os
import logging

logging.root.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s", "%H:%M:%S"
)
stream = logging.StreamHandler()
stream.setFormatter(formatter)

logging.getLogger("").addHandler(stream)

_load_env()


class DevConfig:
    API_KEY = os.environ.get("API_KEY")
    AZURE_VOICE_LANG: str = "zh-CN-YunxiNeural"
    GOOGLE_VOICE_LANG: str = "zh"
    TTS_CHOICE: str = "EDGE"  # "EDGE", "GOOGLE"
    REPLYING: bool = False
    DEVICE_NAME: str = "Built-in Input"

    PREVIOUS_MESSAGES_COUNT: int = 3  # 0 means no contextual conversation
    PREVIOUS_MESSAGES_SAVE_REPLY = True

    SYSTEM_PROMPT = "concisely"
