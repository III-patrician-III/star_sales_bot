import os
from dotenv import load_dotenv

def load_config(path=".env"):
    load_dotenv(path)
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "API_ID": int(os.getenv("API_ID", 0)),
        "API_HASH": os.getenv("API_HASH"),
        "ADMIN_IDS": [int(i) for i in os.getenv("ADMIN_IDS", "").split(",") if i],
        "WALLET_USER_ID": int(os.getenv("WALLET_USER_ID", 0)),
        "CRYPTO_PROJECT_ID": os.getenv("CRYPTO_PROJECT_ID"),
        "CRYPTO_TOKEN": os.getenv("CRYPTO_TOKEN"),
        "CRYPTO_SECRET": os.getenv("CRYPTO_SECRET"),
        "WEBHOOK_URL": os.getenv("WEBHOOK_URL")
    }
