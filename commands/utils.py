from telegram import Message, Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from commands.account import register_account
from data.accounts import ACCOUNTS
from data.schedules import END_TIMES, SCHEDULES, TIMES


async def save_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature phase selection."""
    FORM, FIELD, DATA = [
        context.user_data["FORM"],
        context.user_data["CURRENT_FEATURE"],
        update.message.text,
    ]
    return await save_input(update.message, context, FORM, FIELD, DATA)


async def save_button_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    FORM, FIELD, DATA = query.data.split(":")
    return await save_input(query.message, context, FORM, FIELD, DATA)


async def save_input(
    message: Message,
    context: ContextTypes.DEFAULT_TYPE,
    FORM: str,
    FIELD: str,
    DATA: str,
) -> str:
    context.user_data[FORM][FIELD] = DATA
    return await context.user_data["NEXT_PHASE"](message, context)


def requires_account(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context._user_id in ACCOUNTS:
            return await func(update, context)
        else:
            return await register_account(update, context)

    return wrapper


def get_user_schedule(user_id, context: ContextTypes.DEFAULT_TYPE):
    """Returns the schedule of the user."""
    schedules = SCHEDULES.get_schedule(user_id)
    context.user_data["CALENDER"] = schedules["calendar"]


def get_times_string(column: list):
    """Returns a string of the times in the column."""
    streak = False
    string = ""
    for index, available in enumerate(column):
        if available and not streak:
            string += " " + TIMES[index]
            streak = True
        elif not available and streak:
            string += "\-" + END_TIMES[index] + " "
            streak = False
    if streak:
        string += "\-" + END_TIMES[len(column)]
    if string == "":
        string = "No times selected"
    else:
        string = string.replace("  ", ", ")
        string = string.replace(" ", "")
        string = string.replace(",", ", ")

    return escape_markdown(string)
