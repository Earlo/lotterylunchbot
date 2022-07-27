from data.accounts import ACCOUNTS
from data.pools import POOLS
from data.poolMembers import POOL_MEMBERS
from data.schedules import SCHEDULES, DAYS

from telegram.helpers import escape_markdown

from messages import *

from keyboards import (
    SCHEDULE_KEYBOARD,
    TIME_KEYBOARD,
    OK_KEYBOARD,
    OPTIONS_KEYBOARD,
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


async def schedule_menu_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    if len(options) == 1:
        return await schedule_menu(query, update)
    elif options[1] == "edit":
        await query.edit_message_text(
            text=":D",
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=TIME_KEYBOARD(
                context.user_data.get("MENU_OFFSET", 0),
            ),
        )
    elif options[1] == "move":
        context.user_data["MENU_OFFSET"] = int(options[2])
        await query.edit_message_text(
            text=":D",
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=TIME_KEYBOARD(context.user_data["MENU_OFFSET"]),
        )

    return -1


async def schedule_menu(query: CallbackQuery, update: Update):
    """Displays the schedule menu."""
    user_id = query.from_user.id
    schedules = SCHEDULES.get_schedule(user_id)
    await query.edit_message_text(
        text=SCHEDULE_MENU.format(
            "Name",
            "\n".join(
                [
                    SCHEDULE_MENU_DATE_LINE.format(
                        schedules[d]["weekday"],
                        f'{schedules[d]["start_time"]}-{schedules[d]["end_time"]}'
                        if schedules[d]["available"]
                        else "X",
                    )
                    for d in DAYS
                ]
            ),
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        reply_markup=SCHEDULE_KEYBOARD,
    )
