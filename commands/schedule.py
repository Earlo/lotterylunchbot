from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes

from data.schedules import SCHEDULES
from messages import *
from views.profile.view_profile import view_profile
from views.schedule.view_schedule import view_schedule


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
    await calendar_screen(query, context, options[1:], view_profile)


async def calendar_screen(
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
    options: list,
    on_save: callable,
    pool_id: int | None = None,
):
    print("calendar screen options", options)
    if len(options) == 0:
        pass
    elif options[0] == "move":
        context.user_data["MENU_OFFSET"] = int(options[1])
    elif options[0] == "toggle":
        day_index, time_index = map(int, options[1].split("-"))
        context.user_data["CALENDER"][day_index][time_index] = not context.user_data[
            "CALENDER"
        ][day_index][time_index]
    elif options[0] == "save":
        SCHEDULES.update_schedule(
            query.from_user.id, context.user_data["CALENDER"], pool_id
        )
        return await on_save(query.edit_message_text, context)
    return await view_schedule(query.edit_message_text, context)
