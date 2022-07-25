from telegram.ext import ContextTypes
from telegram import Message, Update

from keyboards import OK_KEYBOARD


async def save_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature phase selection."""
    print("Got text input")
    FORM = context.user_data["FORM"]
    FIELD = context.user_data["CURRENT_FEATURE"]
    DATA = update.message.text
    try:
        return await save_input(update.message, context, FORM, FIELD, DATA)
    except Exception as e:
        print("error", e)


async def save_button_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Parses the CallbackQuery and updates the message text."""
    print("Got button input")
    query = update.callback_query
    await query.answer()
    FORM, FIELD, DATA = query.data.split(":")
    await query.edit_message_text(
        text=f"Selected option: {DATA}", reply_markup=OK_KEYBOARD
    )
    return await save_input(query.message, context, FORM, FIELD, DATA)


async def save_input(
    message: Message,
    context: ContextTypes.DEFAULT_TYPE,
    FORM: str,
    FIELD: str,
    DATA: str,
) -> str:
    context.user_data[FORM][FIELD] = DATA
    print("data is", context.user_data)
    return await context.user_data["NEXT_PHASE"](message, context)
