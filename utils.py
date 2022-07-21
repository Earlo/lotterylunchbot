from asyncio import constants
from data.users import Users

from messages import *

from telegram.ext import ContextTypes
from datetime import timedelta, datetime


async def check_users(context: ContextTypes):
    to_delete = set()
    for u in Users():
        try:
            await context.bot.send_chat_action(u, "typing")
        except Exception as e:
            print("User {} not found".format(u), e)
            to_delete.add(u)
        else:
            Users()[u] = await context.bot.getChat(u)
    for u in to_delete:
        print("Removing", Users()[u]["username"])
        del Users()[u]
    Users().save()


def time_until(clock: str):
    """
    clock: HH:MM
    Returns the amount of time it takes until it's the clock time.
    """
    h, m = clock.split(":")
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    next_time = (
        tomorrow.hour < int(h)
        and now.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
        or tomorrow.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
    )
    # return (next_time - now) / 3000
    return next_time - now
