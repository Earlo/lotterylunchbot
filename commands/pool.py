import os

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    constants,
)
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from commands.schedule import calendar_screen
from commands.utils import requires_account
from data.accounts import ACCOUNTS
from data.poolMembers import POOL_MEMBERS
from data.pools import POOLS
from data.schedules import SCHEDULES
from keyboards import (
    OK_KEYBOARD,
    POOL_CANCEL_KEYBOARD,
    POOL_KEYBOARD,
    POOL_OPTIONS_KEYBOARD,
    POOLS_KEYBOARD,
    RETURN_TO_POOL_MENU_KEYBOARD,
    SUBMIT_CANCEL_KEYBOARD,
    YES_NO_KEYBOARD,
)
from messages import *


async def pool_menu_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    if len(options) == 2:
        # generic pool actions
        action = options[1]
        if action == "browse":
            return await browse_public_pools(query, update)
        if action == "manage":
            return await browse_own_pools(query, update)
        elif action == "join":
            await query.edit_message_text(
                text=JOIN_POOL_PROMT,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=POOL_CANCEL_KEYBOARD,
            )
            context.user_data["FORM"] = "JOIN_POOL"
            context.user_data["JOIN_POOL"] = {}
            context.user_data["CURRENT_FEATURE"] = "name"
            context.user_data["NEXT_PHASE"] = join_private_pool
            return "TYPING"
        elif action == "create":
            await query.edit_message_text(
                text=CREATE_POOL0,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=POOL_CANCEL_KEYBOARD,
            )
            context.user_data["FORM"] = "POOL"
            context.user_data["POOL"] = {}
            context.user_data["CURRENT_FEATURE"] = "name"
            context.user_data["NEXT_PHASE"] = add_name
            return "TYPING"
    elif len(options) > 2:
        # actions for pool -> pool_id
        pool_id = int(options[1])
        action = options[2]
        if action == "view":
            if options[3] == "return":
                return await pool_page(
                    query, update, pool_id, f"{':'.join(options[4:])}"
                )
            return await pool_page(query, update, pool_id)
        elif action == "join":
            POOL_MEMBERS.append(query.from_user.id, pool_id)
        elif action == "leave":
            POOL_MEMBERS.remove_from(query.from_user.id, pool_id)
        elif action == "edit":
            target = options[3]
            await query.edit_message_text(
                text=POOL_EDIT.format(target),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=OK_KEYBOARD,
            )
            context.user_data["FORM"] = "POOL"
            context.user_data["POOL"] = dict(POOLS[pool_id])
            context.user_data["CURRENT_FEATURE"] = target
            context.user_data["NEXT_PHASE"] = check_feature
            return "TYPING"
        elif action == "schedule":
            if "CALENDER" not in context.user_data:
                schedules = SCHEDULES.get_schedule(update.effective_user.id, pool_id)
                context.user_data["CALENDER"] = schedules["calendar"]
            if "MENU_OFFSET" not in context.user_data:
                context.user_data["MENU_OFFSET"] = 0
            print("with", options[:3])
            return await calendar_screen(
                query, context, pool_id, options[3:], pool_page_view, pool_id=pool_id
            )
        elif action == "toggle":
            field = options[3]
            value = options[4]
            POOLS.update(pool_id, field, value)
        elif action == "delete":
            del POOLS[pool_id]
            return await browse_public_pools(query, update)
    return await pools_menu(query, update)


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


async def join_private_pool(message: Message, context: ContextTypes.DEFAULT_TYPE):
    """Add information about the pool."""
    pool_name = context.user_data["JOIN_POOL"]["name"]
    pool = POOLS.get_by_name(pool_name)
    if pool is None:
        await message.reply_markdown_v2(
            text=JOIN_POOL_FAIL.format(escape_markdown(pool_name, version=2)),
            reply_markup=RETURN_TO_POOL_MENU_KEYBOARD,
        )
        return -1
    else:
        await pool_page_view(message.reply_text, message.from_user.id, pool)
        return -1


@requires_account
async def create_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_markdown_v2(
        text=CREATE_POOL0,
        reply_markup=POOL_CANCEL_KEYBOARD,
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
            await query.delete_message()
            return await check(query.message, context)
    elif user_data["CHOICE"] == "submit_pool":
        if DATA == "True":
            pool = POOLS.append(user_data["POOL"])
            POOL_MEMBERS.append(context._user_id, pool["id"], True)
            await pool_page_view(query.edit_message_text, context._user_id, pool)
        else:
            await query.edit_message_text(
                text=CREATE_POOL_CANCEL,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                reply_markup=RETURN_TO_POOL_MENU_KEYBOARD,
            )
    elif user_data["CHOICE"] == "submit_pool_edit":
        if user_data["POOL"]["id"]:
            # Yrjistä :D
            pool = POOLS[user_data["POOL"]["id"]] = user_data["POOL"]
            await pool_page_view(query.edit_message_text, context._user_id, pool)
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
        text=escape_markdown(
            POOL_EDIT_CONFIRM.format(
                context.user_data["POOL"]["name"],
                context.user_data["CURRENT_FEATURE"],
                context.user_data["POOL"][context.user_data["CURRENT_FEATURE"]],
            ),
            version=2,
        ),
        reply_markup=SUBMIT_CANCEL_KEYBOARD,
    )
    return "CONFIRM"


async def browse_public_pools(query: CallbackQuery, update: Update) -> None:
    await query.edit_message_text(
        text=POOL_BROWSE_PUBLIC,
        reply_markup=POOLS_KEYBOARD(
            extra=":return:pool_menu:browse", pools_shown=POOLS.public_pools()
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )


async def browse_own_pools(query: CallbackQuery, update: Update) -> None:
    pools = POOLS.pools_of(update.effective_user.id)
    await query.edit_message_text(
        text=POOL_BROWSE_PUBLIC,
        reply_markup=POOLS_KEYBOARD(
            extra=":return:pool_menu:manage", pools_shown=pools
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )


async def pools_menu(query: CallbackQuery, update: Update) -> None:
    pools = POOLS.pools_of(update.effective_user.id)
    await query.edit_message_text(
        text=POOL_EXPLANATION,
        reply_markup=POOL_OPTIONS_KEYBOARD(len(pools) > 0),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return -1


async def pool_page(
    query: CallbackQuery, update: Update, pool_id: int, return_page: str | None = None
) -> None:
    return await pool_page_view(
        query.edit_message_text, query.from_user.id, POOLS[pool_id], return_page
    )


async def pool_page_view(reply, user_id, pool, return_page: str | None = None):
    is_member, is_admin, count = POOL_MEMBERS.get_meta(user_id, pool["id"])
    await reply(
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
        reply_markup=POOL_KEYBOARD(
            pool,
            is_member,
            is_admin or user_id == int(os.environ.get("ADMIN_ACCOUNT_ID")),
            return_page,
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
