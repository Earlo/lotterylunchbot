from data.accounts import ACCOUNTS
from data.pools import POOLS
from data.poolMembers import POOL_MEMBERS

from telegram.helpers import escape_markdown

from messages import *

from keyboards import (
    YES_NO_KEYBOARD,
    SUBMIT_CANCEL_KEYBOARD,
    OK_KEYBOARD,
    OPTIONS_KEYBOARD,
    POOL_KEYBOARD,
    POOLS_KEYBOARD,
)

from telegram import (
    Message,
    Update,
    constants,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from commands.utils import requires_account


async def pool_menu_callbacks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    if len(options) == 1:
        return await pools_menu(query, update)
    pool_id = int(options[1])
    if len(options) > 2:
        action = options[2]
        if action == "join":
            POOL_MEMBERS.append(query.from_user.id, pool_id)
        elif action == "leave":
            POOL_MEMBERS.remove_from(query.from_user.id, pool_id)
        elif action == "edit":
            target = options[3]
            if target == "name":
                await query.edit_message_text(
                    text=POOL_EDIT_NAME,
                    parse_mode=constants.ParseMode.MARKDOWN_V2,
                    reply_markup=OK_KEYBOARD,
                )
                context.user_data["FORM"] = "POOL"
                context.user_data["POOL"] = dict(POOLS[pool_id])
                context.user_data["CURRENT_FEATURE"] = "name"
                context.user_data["NEXT_PHASE"] = check_feature
                return "TYPING"
    return await pool_menu(query, update, pool_id)


@requires_account
async def join_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    pool_name = update.message.text.split(" ")[1]
    pool = POOLS.get_by_name(pool_name)
    if pool == None:
        await update.message.reply_markdown_v2(
            text=JOIN_POOL_FAIL.format(escape_markdown(pool_name, version=2)),
            reply_markup=OK_KEYBOARD,
        )
    else:
        response = POOL_MEMBERS.append(context._user_id, pool["id"])
        if response == None:
            await update.message.reply_markdown_v2(
                text=JOIN_POOL_ALREADY_MEMBER.format(
                    escape_markdown(pool_name, version=2)
                ),
                reply_markup=OK_KEYBOARD,
            )
        else:
            await update.message.reply_markdown_v2(
                text=JOIN_POOL_SUCCESS.format(escape_markdown(pool_name, version=2)),
                reply_markup=OK_KEYBOARD,
            )
    return -1


@requires_account
async def create_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    account = ACCOUNTS[context._user_id]
    await update.message.reply_markdown_v2(
        text=CREATE_POOL0.format(escape_markdown(account["first_name"], version=2)),
    )
    context.user_data["FORM"] = "POOL"
    context.user_data["POOL"] = {}
    context.user_data["CURRENT_FEATURE"] = "name"
    context.user_data["NEXT_PHASE"] = add_name
    return "TYPING"


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
            pool = POOLS.append(user_data["POOL"])
            POOL_MEMBERS.append(context._user_id, pool["id"], True)
            await update.callback_query.edit_message_text(
                text=CREATE_POOL5.format(
                    escape_markdown(pool["name"], version=2),
                    escape_markdown(pool["description"], version=2),
                    pool["public"],
                ),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=OK_KEYBOARD,
            )
    elif user_data["CHOICE"] == "submit_pool_edit":
        if user_data["POOL"]["id"]:
            # Yrjistä :D
            pool = POOLS[user_data["POOL"]["id"]] = user_data["POOL"]
            await update.callback_query.edit_message_text(
                text=EDIT_POOL_DONE.format(
                    escape_markdown(pool["name"], version=2),
                    escape_markdown(pool["description"], version=2),
                    pool["public"],
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
            escape_markdown(context.user_data["POOL"]["name"], version=2)
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


async def check_feature(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data["CHOICE"] = "submit_pool_edit"
    await message.reply_markdown_v2(
        text=f"change {context.user_data['POOL']['name']} {context.user_data['CURRENT_FEATURE']} to {context.user_data['POOL'][context.user_data['CURRENT_FEATURE']]}?",
        reply_markup=SUBMIT_CANCEL_KEYBOARD,
    )
    return "CONFIRM"


async def pools_menu(query: CallbackQuery, update: Update) -> None:
    await query.edit_message_text(
        text=POOL_OPTIONS.format(
            escape_markdown(query.from_user.first_name, version=2)
        ),
        reply_markup=POOLS_KEYBOARD(),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )


async def pool_menu(query: CallbackQuery, update: Update, pool_id: int) -> None:
    user_id = query.from_user.id
    pool = POOLS[pool_id]
    is_member, is_admin, count = POOL_MEMBERS.get_meta(user_id, pool["id"])
    await query.edit_message_text(
        text=POOL_DESCRIPTION.format(
            escape_markdown(pool["name"], version=2),
            escape_markdown(pool["description"], version=2),
            "The group is public\." if pool["public"] else "The group is private\.",
            count,
            "You're the admin"
            if is_admin
            else "You're a member"
            if is_member
            else "You're not a member",
        ),
        reply_markup=POOL_KEYBOARD(pool, is_member, is_admin),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
