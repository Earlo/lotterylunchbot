from telegram import CallbackQuery, Update, constants
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from commands.general import send_profile_menu
from data.schedules import SCHEDULES
from keyboards import TIME_KEYBOARD
from messages import *


async def schedule_menu_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    if "CALENDER" not in context.user_data:
        schedules = SCHEDULES.get_schedule(update.effective_user.id)
        context.user_data["CALENDER"] = schedules["calendar"]
    if "MENU_OFFSET" not in context.user_data:
        context.user_data["MENU_OFFSET"] = 0

    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    if len(options) == 1:
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
        return await send_profile_menu(query.edit_message_text, context)
    return -1
