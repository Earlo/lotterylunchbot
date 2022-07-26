from asyncio import constants
from data.accounts import ACCOUNTS

from messages import *

from telegram.ext import ContextTypes
from datetime import timedelta, datetime


async def check_accounts(context: ContextTypes):
    to_delete = set()
    for u in ACCOUNTS:
        try:
            await context.bot.send_chat_action(u, "typing")
        except Exception as e:
            print("User {} not found".format(u), e)
            to_delete.add(u)
        else:
            ACCOUNTS[u] = await context.bot.getChat(u)
    for u in to_delete:
        print("Removing", ACCOUNTS[u]["username"])
        del ACCOUNTS[u]
    ACCOUNTS.save()


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
