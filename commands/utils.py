from telegram.ext import ContextTypes
from telegram import Update


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature phase selection."""
    user_data = context.user_data
    print(
        "Doing save intput",
        user_data["FEATURES"],
        user_data["CURRENT_FEATURE"],
        user_data["NEXT_PHASE"],
    )
    user_data["FEATURES"][user_data["CURRENT_FEATURE"]] = update.message.text
    return await user_data["NEXT_PHASE"](update, context)
