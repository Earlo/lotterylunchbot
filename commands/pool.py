from data.users import Users
from data.pools import Pools
from data.schedules import Schedules

from messages import *

from keyboards import HOMEKEYBOARD, OPTIONS_KEYBOARD, POOLS_KEYBOARD, OK_KEYBOARD
from telegram import (
    Update,
    CallbackQuery,
    constants,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackContext

from commands.general import register_user


async def create_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    USERS = Users()
    userid = str(update.message.from_user.id)
    if userid in USERS:
        user = USERS[userid]
        await update.message.reply_text(
            text=CREATE_POOL0.format(user["first_name"]),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )

        user_data = context.user_data

        user_data["FEATURES"] = {}
        user_data["CURRENT_FEATURE"] = "name"
        user_data["NEXT_PHASE"] = adding_name
        return "TYPING"
    else:
        # Not registered, register first
        register_user(update, context)


async def adding_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    print("Adding name", context.user_data)
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
    await update.message.reply_text(
        text=CREATE_POOL1.format(context.user_data["FEATURES"]["name"]),
        reply_markup=keyboard,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return "SELECTING"


async def pool_creation_form(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()
    FORM, FIELD, DATA = query.data.split(":")
    if FORM == "POOL":
        context.user_data["FEATURES"][FIELD] = DATA

    await query.edit_message_text(
        text=f"Selected option: {DATA}", reply_markup=OK_KEYBOARD
    )

    return ""
