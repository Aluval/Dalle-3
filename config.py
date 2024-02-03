from os import environ

import requests

API_ID = int(environ.get("API_ID", 0))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
BOT_USERNAME = environ.get("BOT_USERNAME", "")
OWNER_ID = environ.get("OWNER_ID", "")
FORCESUB_CHANNEL = environ.get("FORCESUB_CHANNEL", "")
FORCESUB_CHANNEL_UNAME = environ.get("FORCESUB_CHANNEL_UNAME", "")
BOTOWNER_UNAME = environ.get("BOTOWNER_UNAME", "")


