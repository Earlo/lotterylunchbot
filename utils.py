from asyncio import constants
from data.accounts import ACCOUNTS
from data.schedules import SCHEDULES

from messages import *

from telegram.ext import ContextTypes
from datetime import timedelta, datetime


async def check_accounts(context: ContextTypes):
    to_delete = set()
    for account_id in ACCOUNTS:
        try:
            await context.bot.send_chat_action(account_id, "typing")
        except Exception as e:
            print("User {} not found".format(account_id), e)
            to_delete.add(account_id)
        else:
            ACCOUNTS.create_account(account_id, await context.bot.getChat(account_id))
    for account_id in to_delete:
        del ACCOUNTS[account_id]
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


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
