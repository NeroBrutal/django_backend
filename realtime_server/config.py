import os
from dotenv import load_dotenv  ##type: ignore

load_dotenv()  # ✅ This loads variables from .env into os.environ


class Config:
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    if not WEBHOOK_URL:
        raise RuntimeError("WEBHOOK_URL environment variable not set")
