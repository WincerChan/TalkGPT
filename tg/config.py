from dotenv import load_dotenv as _load_env
import os
import logging

logging.root.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
stream = logging.StreamHandler()
stream.setFormatter(formatter)

logging.getLogger("").addHandler(stream)

_load_env()


class DevConfig:
    API_KEY = os.environ.get("API_KEY")
    AZURE_VOICE_LANG = "zh-CN-XiaoxiaoNeural"
    GOOGLE_VOICE_LANG = "en"
    TTS_CHOICE = "EDGE"  # "GOOGLE", "SYSTEM"
