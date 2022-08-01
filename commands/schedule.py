from data.accounts import ACCOUNTS
from data.pools import POOLS
from data.poolMembers import POOL_MEMBERS
from data.schedules import SCHEDULES, DAYS, TIMES, END_TIMES

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


def get_user_schedule(user_id, context: ContextTypes.DEFAULT_TYPE):
    """Returns the schedule of the user."""
    schedules = SCHEDULES.get_schedule(user_id)
    context.user_data["CALENDER"] = schedules["calendar"]


async def schedule_menu_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    if "CALENDER" not in context.user_data:
        get_user_schedule(update.effective_user.id, context)
    if "MENU_OFFSET" not in context.user_data:
        context.user_data["MENU_OFFSET"] = 0

    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    if len(options) == 1:
        return await schedule_menu(query, context)
    elif options[1] == "edit":
        await query.edit_message_text(
            text=SCHEDULE_EDIT_INSTRUCTIONS,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=TIME_KEYBOARD(
                context.user_data["MENU_OFFSET"], context.user_data["CALENDER"]
            ),
        )
    elif options[1] == "move":
        context.user_data["MENU_OFFSET"] = int(options[2])
        await query.edit_message_text(
            text=SCHEDULE_EDIT_INSTRUCTIONS,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=TIME_KEYBOARD(
                context.user_data["MENU_OFFSET"], context.user_data["CALENDER"]
            ),
        )
    elif options[1] == "toggle":
        day_index, time_index = map(int, options[2].split("-"))
        context.user_data["CALENDER"][day_index][time_index] = not context.user_data[
            "CALENDER"
        ][day_index][time_index]
        await query.edit_message_text(
            text=SCHEDULE_EDIT_INSTRUCTIONS,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=TIME_KEYBOARD(
                context.user_data["MENU_OFFSET"], context.user_data["CALENDER"]
            ),
        )
    elif options[1] == "save":
        SCHEDULES.update_schedule(
            update.effective_user.id, context.user_data["CALENDER"]
        )
        return await schedule_menu(query, context)

    return -1


async def schedule_menu(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    """Displays the schedule menu."""
    await query.edit_message_text(
        text=SCHEDULE_MENU.format(
            query.from_user.first_name,
            "\n".join(
                [
                    SCHEDULE_MENU_DATE_LINE.format(
                        DAYS[day_index],
                        get_times_string(column),
                    )
                    for day_index, column in enumerate(context.user_data["CALENDER"])
                ]
            ),
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        reply_markup=SCHEDULE_KEYBOARD,
    )


def get_times_string(column):
    """Returns a string of the times in the column."""
    streak = False
    string = ""
    for index, available in enumerate(column):
        if available and not streak:
            string += " " + TIMES[index]
            streak = True
        elif not available and streak:
            string += "-" + END_TIMES[index] + " "
            streak = False
    if streak:
        string += "-" + END_TIMES[len(column)]

    string = string.replace("  ", ", ")
    string = string.replace(" ", "")
    return string.replace(",", ", ")