from tg.config import DevConfig

match DevConfig.TTS_CHOICE:
    case "EDGE":
        from .azure_tts import Speech
    case "GOOGLE":
        from .google_tts import Speech
    case x:
        raise RuntimeError(f"Error choice {x}")
