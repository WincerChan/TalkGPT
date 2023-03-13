from tg.config import DevConfig

match DevConfig.TTS_CHOICE:
    case "EDGE":
        from .azure_tts import speak_text
    case "GOOGLE":
        from .google_tts import speak_text
    case _:
        from .native_tts import speak_text
