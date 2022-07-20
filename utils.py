from asyncio import constants
from data.users import Users

from messages import *

from telegram.ext import ContextTypes


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
