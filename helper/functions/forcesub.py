import os
import random
import shutil
import string

from pyrogram.enums import ChatMemberStatus, ChatType, ParseMode
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import *

async def forcesub(client, message: Message) -> bool:
    """
    Returns True if user is subscribed to Said Channel else returns False
    """
    if (
        FORCESUB_ENABLE
        and (FORCESUB_CHANNEL and FORCESUB_CHANNEL_UNAME and BOTOWNER_UNAME) is not None
        and message.chat.type
        not in [ChatType.SUPERGROUP, ChatType.CHANNEL, ChatType.GROUP, ChatType.BOT]
    ):
        try:
            user = await client.get_chat_member(FORCESUB_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.chat.id,
                    text=f"<b><i>Sorry, You are banned from the Channel {FORCESUB_CHANNEL_UNAME} and hence cannot use the Bot.\nContact {BOTOWNER_UNAME}</i></b>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                return False
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.chat.id,
                text="<b>Join the channel below to use the Bot 🔐</b>\n\n<i>Resend the command along with link after you have successfully joined...</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Join🔓", url=f"https://t.me/{FORCESUB_CHANNEL_UNAME}"
                            ),
                            InlineKeyboardButton(
                                "Owner🔓", url=f"https://t.me/{BOTOWNER_UNAME}"
                            ),
                        ]
                    ]
                ),
                parse_mode=ParseMode.HTML,
            )
            return False
        except Exception as err:
            await client.send_message(
                chat_id=message.chat.id,
                text=f"<i>Something went wrong in ForceSub Module\nContact {BOTOWNER_UNAME}</i>\n\n{err}",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            return False
    return True
