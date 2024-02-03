#Sᴜɴʀɪsᴇs Hᴀʀsʜᴀ 𝟸𝟺 🇮🇳 ᵀᴱᴸ
import base64
import json
import os
import shutil
import threading
import requests
from pyrogram.types import (InlineKeyboardButton,  InlineKeyboardMarkup)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from config import *
from pyrogram.types import *
from pyrogram.types import InputMediaPhoto, Message
#from bot.helper import ratelimit, user_commands
from helper.functions import forcesub

commands = ["dalle", f"dalle@{BOT_USERNAME}"]

#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24

# Initialize the Pyrogram client
app = Client(
    "DalleMini24",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("Bot Started!💎 © t.me/Sunrises_24")
                           
@app.on_message(filters.command(["start"]))
def start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	app.send_message(message.chat.id,"Hi I am Dalle-Mini Bot, i can send request to https://www.craiyon.com/ with text prompt describing image and get you the results here\n\nUse /dalle command with the text prompt")

# dalle command
@app.on_message(filters.command(["dalle"]))
def getpompt(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# getting prompt from the text
	try:
		prompt = message.text.split("/dalle ")[1]
	except:
		app.send_message(message.chat.id,'Send Prompt with Command,\nUssage : "/dalle high defination studio image of pokemon"')
		return	

	# threding	
	app.send_message(message.chat.id,"Prompt received and Request is sent. Waiting time is 2-3 mins")
	ai = threading.Thread(target=lambda:genrateimages(message,prompt),daemon=True)
	ai.start()

# request data
reqUrl = "https://backend.craiyon.com/generate"
headersList = {"authority": "backend.craiyon.com", "accept": "application/json", "accept-language": "en-US,en;q=0.9", "cache-control": "no-cache", "content-type": "application/json", "dnt": "1", "origin": "https://www.craiyon.com", "pragma": "no-cache", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "Linux", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-site", "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
#pretext = "data:image/jpeg;base64,"

# getting images and uploding
def genrateimages(message,prompt):

	# getting the response
	import json

payload = json.dumps({"prompt": prompt})

try:
    response = requests.post(reqUrl, data=payload, headers=headersList)
    response.raise_for_status()  # Check for HTTP errors

    try:
        json_data = response.json()       
        os.mkdir(str(message.id))

        i = 1
        for ele in json_data.get("images", []):
            image = base64.b64decode(ele.replace('\\n', ''))
            with open(f"{message.id}/{i}.jpeg", "wb") as file:
                file.write(image)
            i += 1

    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
	
	# sending images
	       app.send_media_group(message.chat.id,
               [
                InputMediaPhoto(f"{message.id}/1.jpeg", caption=prompt),
                InputMediaPhoto(f"{message.id}/2.jpeg", caption=prompt),
                InputMediaPhoto(f"{message.id}/3.jpeg", caption=prompt),
		InputMediaPhoto(f"{message.id}/4.jpeg", caption=prompt),
		InputMediaPhoto(f"{message.id}/5.jpeg", caption=prompt),
		InputMediaPhoto(f"{message.id}/6.jpeg", caption=prompt),
		InputMediaPhoto(f"{message.id}/7.jpeg", caption=prompt),
		InputMediaPhoto(f"{message.id}/8.jpeg", caption=prompt),
		InputMediaPhoto(f"{message.id}/9.jpeg", caption=prompt)
                ]
						)

	# archiving and uploding
	shutil.make_archive(prompt,"zip",str(message.id))
	app.send_document(message.chat.id,document=f"{prompt}.zip",caption=f'{prompt}\n\n(Archive for Uncompressed Images)')
	os.remove(f"{prompt}.zip")
	shutil.rmtree(str(message.id))


# Run the bot
app.run()
