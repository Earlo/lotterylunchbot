from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from data.accounts import ACCOUNTS
from keyboards import OPTIONS_KEYBOARD
from messages import GREETING_NEW


async def register_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userid = update.message.from_user.id
    ACCOUNTS.create_account(userid, update.message.from_user)
    await update.message.reply_markdown_v2(
        text=GREETING_NEW.format(
            escape_markdown(update.message.from_user.first_name, version=2)
        ),
        reply_markup=OPTIONS_KEYBOARD,
    )
