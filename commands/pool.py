from sqlalchemy import true
from data.accounts import ACCOUNTS
from data.pools import POOLS
from data.accountsPools import ACCOUNTS_POOLS

from telegram.helpers import escape_markdown

from messages import *

from keyboards import YES_NO_KEYBOARD, SUBMIT_CANCEL_KEYBOARD, OK_KEYBOARD

from telegram import (
    Message,
    Update,
    constants,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackContext

from commands.general import register_account


async def create_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    userid = context._user_id
    if userid in ACCOUNTS:
        account = ACCOUNTS[userid]
        await update.message.reply_markdown_v2(
            text=CREATE_POOL0.format(escape_markdown(account["first_name"]), version=2),
        )
        context.user_data["FORM"] = "POOL"
        context.user_data["POOL"] = {}
        context.user_data["CURRENT_FEATURE"] = "name"
        context.user_data["NEXT_PHASE"] = add_name
        return "TYPING"
    else:
        # Not registered, register first
        await register_account(update, context)


async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    query = update.callback_query
    user_data = context.user_data
    await query.answer()
    DATA = query.data
    if user_data["CHOICE"] == "add_description":
        if DATA == "True":
            await update.callback_query.edit_message_text(
                text=CREATE_POOL3,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
            user_data["CURRENT_FEATURE"] = "description"
            user_data["NEXT_PHASE"] = check
            return "TYPING"
        else:
            user_data["POOL"]["description"] = ""
            return await check(query.message, context)
    elif user_data["CHOICE"] == "submit_pool":
        if DATA == "True":
            new_pool = POOLS.append(user_data["POOL"])
            ACCOUNTS_POOLS.append(context._user_id, new_pool["id"], True)
            await update.callback_query.edit_message_text(
                text=CREATE_POOL5.format(
                    escape_markdown(user_data["POOL"]["name"], version=2),
                    escape_markdown(user_data["POOL"]["description"], version=2),
                    escape_markdown(user_data["POOL"]["public"], version=2),
                ),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=OK_KEYBOARD,
            )
        return -1


async def add_name(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Public",
                    callback_data="POOL:public:True",
                ),
                InlineKeyboardButton(
                    text="Private",
                    callback_data="POOL:public:False",
                ),
            ]
        ]
    )
    await message.reply_markdown_v2(
        text=CREATE_POOL1.format(
            escape_markdown(context.user_data["POOL"]["name"]), version=2
        ),
        reply_markup=keyboard,
    )
    context.user_data["NEXT_PHASE"] = add_description
    return "SELECTING"


async def add_description(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about the pool."""
    context.user_data["CHOICE"] = "add_description"
    await message.edit_text(
        text=CREATE_POOL2,
        reply_markup=YES_NO_KEYBOARD,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return "CONFIRM"


async def check(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data["CHOICE"] = "submit_pool"
    await message.reply_markdown_v2(
        text=CREATE_POOL4.format(
            escape_markdown(context.user_data["POOL"]["name"], version=2),
            escape_markdown(context.user_data["POOL"]["description"], version=2),
            escape_markdown(context.user_data["POOL"]["public"], version=2),
        ),
        reply_markup=SUBMIT_CANCEL_KEYBOARD,
    )
    return "CONFIRM"
