from dotenv import load_dotenv
import os

load_dotenv("config.env")

TEL_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID_IMGUR = os.getenv("API_TOKEN")
WHITE_LIST_CHATS = [int(x) for x in os.getenv("WHITE_LIST_CHATS").split(",") if x.strip()]
WHITE_LIST_USERS = [int(x) for x in os.getenv("WHITE_LIST_USERS").split(",") if x.strip()]

WHITE_LIST_ENABLE=False
MAX_CHARS=4096
MAX_REQUESTS=5
ROLLBACK_TIME=120
