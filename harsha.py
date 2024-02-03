#Sᴜɴʀɪsᴇs Hᴀʀsʜᴀ 𝟸𝟺 🇮🇳 ᵀᴱᴸ
import base64
import json
import os
import shutil
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
    "image_editor_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("Bot Started!🦋 © t.me/Sunrises_24")
                           
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        f"Hello {message.from_user.first_name}❤️ Welcome! Send me an text",reply_to_message_id = message.id ,  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝐔𝐏𝐃𝐀𝐓𝐄𝐒 📢" ,url=f"https://t.me/Sunrises24BotUpdates") ],
                    [
                    InlineKeyboardButton("𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑 🧑🏻‍💻" ,url="https://t.me/Sunrises_24") ],
                    [
                    InlineKeyboardButton("𝐂𝐇𝐀𝐍𝐍𝐄𝐋 🎞️" ,url="https://t.me/sunriseseditsoffical6") ]                               
            ]))
    
@app.on_message(filters.command("dalle"))
async def dalle(client, message: Message):
    """
    DALL·E Mini - Generate images from a text prompt
    """
    global query   
    reply_to = message.reply_to_message

    if len(message.command) > 1:
        query = message.text.split("/dalle ")[1]
    elif reply_to is not None:
        query = reply_to.text
    elif len(message.command) < 2 or reply_to is None:
        err = "<b><i>Please send a query or reply to an query to proceed!</i></b>"
        await message.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return
    try:
        await generateimages(client, message, query)
except Exception as e:
        error_message = f"<b>Error encountered while generating Image from DALLE-Mini:</b> {str(e)}"
        await message.reply_text(text=error_message, disable_web_page_preview=True, quote=True)
        return


reqUrl = "https://backend.craiyon.com/generate"
headersList = {
    "authority": "backend.craiyon.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://www.craiyon.com",
    "pragma": "no-cache",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


async def generateimages(client, message, query):

    payload = json.dumps({"prompt": query})
    response = requests.request(
        "POST", reqUrl, data=payload, headers=headersList
    ).json()
    os.mkdir(str(message.id))

    i = 1
    for ele in response["images"]:
        image = base64.b64decode(ele.replace("\\n", ""))
        with open(f"{message.id}/{i}.jpeg", "wb") as file:
            file.write(image)
        i = i + 1

    await client.send_media_group(
        chat_id=message.chat.id,
        media=[
            InputMediaPhoto(f"{message.id}/1.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/2.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/3.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/4.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/5.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/6.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/7.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/8.jpeg", caption=query),
            InputMediaPhoto(f"{message.id}/9.jpeg", caption=query),
        ],
    )

    shutil.make_archive(query, "zip", str(message.id))
    await client.send_document(
        chat_id=message.chat.id,
        document=f"{query}.zip",
        caption=f"{query}\n\n(Archive for Uncompressed Images)",
    )
    os.remove(f"{query}.zip")
    shutil.rmtree(str(message.id))

# Run the bot
app.run()
