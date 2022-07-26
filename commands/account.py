from data.accounts import ACCOUNTS

from messages import *

from keyboards import HOMEKEYBOARD
from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown


async def register_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userid = update.message.from_user.id
    ACCOUNTS[userid] = update.message.from_user
    await update.message.reply_markdown_v2(
        text=GREETING_NEW.format(
            escape_markdown(update.message.from_user.first_name, version=2)
        ),
        reply_markup=HOMEKEYBOARD,
    )
