import asyncio
from functools import wraps
from typing import Callable, Union

from pyrogram import Client
from pyrogram.types import CallbackQuery, Message


from config import *
from helper.ratelimiter import RateLimiter

ratelimiter = RateLimiter()

def ratelimit(func: Callable) -> Callable:
    """
    Restricts user's from spamming commands or pressing buttons multiple times
    using leaky bucket algorithm and pyrate_limiter.
    """

    @wraps(func)
    async def decorator(client: Client, update: Union[Message, CallbackQuery]):
        userid = update.from_user.id
        is_limited = await ratelimiter.acquire(userid)
        if is_limited and userid not in warned_users:
            if isinstance(update, Message):
                await update.reply_text(warning_message)
                warned_users[userid] = 1
                return
            elif isinstance(update, CallbackQuery):
                await update.answer(warning_message, show_alert=True)
                warned_users[userid] = 1
                return
        elif is_limited and userid in warned_users:
            pass
        else:
            return await func(client, update)

    return decorator


def user_commands(func: Callable) -> Callable:
    """
    Allows all user's' to use publicly available commands
    """

    @wraps(func)
    async def decorator(client: Client, message: Message):
        return await func(client, message)

    return decorator
