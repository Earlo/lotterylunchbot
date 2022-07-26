from data.users import USERS
from data.pools import POOLS
from data.schedules import Schedules

from telegram.helpers import escape_markdown

from messages import *

from keyboards import (
    HOMEKEYBOARD,
    OPTIONS_KEYBOARD,
    POOLS_KEYBOARD,
    OK_KEYBOARD,
    YES_NO_KEYBOARD,
    CLEANUP,
    SUBMIT_CANCEL_KEYBOARD,
)
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
    userid = str(update.message.from_user.id)
    if userid in USERS:
        user = USERS[userid]
        await update.message.reply_text(
            text=escape_markdown(CREATE_POOL0.format(user["first_name"]), version=2),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
        user_data = context.user_data
        user_data["FORM"] = "POOL"
        user_data["POOL"] = {"owner": userid}
        user_data["CURRENT_FEATURE"] = "name"
        user_data["NEXT_PHASE"] = add_name
        return "TYPING"
    else:
        # Not registered, register first
        register_user(update, context)


async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about yourself."""
    query = update.callback_query
    await query.answer()
    DATA = query.data
    if context.user_data["CHOICE"] == "add_description":
        if DATA == "True":
            await update.callback_query.edit_message_text(
                text=escape_markdown(CREATE_POOL3, version=2),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
            context.user_data["CURRENT_FEATURE"] = "description"
            context.user_data["NEXT_PHASE"] = check
            return "TYPING"
        else:
            return await check(query.message)
    elif context.user_data["CHOICE"] == "submit_pool":
        if DATA == "True":
            POOLS.append(context.user_data["POOL"])
            await update.callback_query.edit_message_text(
                text=escape_markdown(
                    CREATE_POOL5.format(
                        context.user_data["POOL"]["name"],
                        context.user_data["POOL"]["description"],
                        context.user_data["POOL"]["public"],
                    ),
                    version=2,
                ),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=OK_KEYBOARD,
            )
        return "HOME"


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
    await message.reply_text(
        text=escape_markdown(
            CREATE_POOL1.format(context.user_data["POOL"]["name"]), version=2
        ),
        reply_markup=keyboard,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    context.user_data["NEXT_PHASE"] = add_description
    return "SELECTING"


async def add_description(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Add information about the pool."""
    context.user_data["CHOICE"] = "add_description"
    await message.edit_text(
        text=escape_markdown(CREATE_POOL2, version=2),
        reply_markup=YES_NO_KEYBOARD,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return "CONFIRM"


async def check(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data["CHOICE"] = "submit_pool"
    await message.reply_text(
        text=escape_markdown(
            CREATE_POOL4.format(
                context.user_data["POOL"]["name"],
                context.user_data["POOL"]["description"],
                context.user_data["POOL"]["public"],
            ),
            version=2,
        ),
        reply_markup=SUBMIT_CANCEL_KEYBOARD,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return "CONFIRM"
