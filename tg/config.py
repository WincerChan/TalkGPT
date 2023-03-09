from dotenv import load_dotenv
import os

load_dotenv()


class DevConfig:
    API_KEY = os.environ.get("API_KEY")
