from data.users import Users
from data.pools import Pools
from data.schedules import Schedules
import json

from telegram.helpers import escape_markdown

from messages import *

from keyboards import HOMEKEYBOARD, OPTIONS_KEYBOARD, POOLS_KEYBOARD, OK_KEYBOARD
from telegram import (
    Message,
    Update,
    constants,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackContext

from commands.general import register_user


async def create_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    USERS = Users()
    userid = str(update.message.from_user.id)
    if userid in USERS:
        user = USERS[userid]
        await update.message.reply_text(
            text=CREATE_POOL0.format(user["first_name"]),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )

        user_data = context.user_data
        user_data["FORM"] = "POOL"
        user_data["POOL"] = {}
        user_data["CURRENT_FEATURE"] = "name"
        user_data["NEXT_PHASE"] = adding_name
        return "TYPING"
    else:
        # Not registered, register first
        register_user(update, context)


async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    query = update.callback_query
    user_data = context.user_data
    await query.answer()
    CHOICE, DATA = query.data.split(":")
    if CHOICE == "add_description":
        if DATA == "True":
            await update.callback_query.edit_message_text(
                text=CREATE_POOL3,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
            user_data["CURRENT_FEATURE"] = "description"
            user_data["NEXT_PHASE"] = check
            return "TYPING"
        else:
            return await check(query.message)


async def adding_name(message: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
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
    await message.reply_text(
        text=CREATE_POOL1.format(context.user_data["POOL"]["name"]),
        reply_markup=keyboard,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    context.user_data["NEXT_PHASE"] = add_description
    return "SELECTING"


async def add_description(message: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Yes",
                    callback_data="add_description:True",
                ),
                InlineKeyboardButton(
                    text="No",
                    callback_data="add_description:False",
                ),
            ]
        ]
    )
    await message.edit_text(
        text=CREATE_POOL2,
        reply_markup=keyboard,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return "CONFIRM"


async def check(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    await message.reply_text(
        text=escape_markdown(
            CREATE_POOL4.format(
                context.user_data["POOL"]["name"],
                context.user_data["POOL"]["description"],
                context.user_data["POOL"]["public"],
            ),
            version=2,
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return "HOME"
