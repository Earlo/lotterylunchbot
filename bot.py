import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands.general import (
    debug_raffle_pairs,
    home,
    inline_menu,
    raffle_pairs,
    remind,
    skip,
)
from commands.pool import choose, create_pool, join_pool, pool_menu_callbacks
from commands.schedule import schedule_menu_callbacks
from commands.utils import save_button_input, save_text_input
from data.accounts import ACCOUNTS
from data.poolMembers import POOL_MEMBERS
from data.pools import POOLS
from data.schedules import SCHEDULES
from utils import time_until

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error(bot, update):
    """Log Errors caused by Updates"""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    """
    Main function.
    """
    application = Application.builder().token(os.getenv("TOKEN")).build()
    # Get the dispatcher to register handlers
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", home),
            CommandHandler("skip", skip),
            CommandHandler("debugraffle", debug_raffle_pairs),
        ],
        states={},
        fallbacks=[CommandHandler("start", home)],
        per_message=False,
        per_user=True,
    )

    pool_handler = ConversationHandler(
        entry_points=[
            CommandHandler("create_pool", create_pool),
            CommandHandler("join", join_pool),
            CallbackQueryHandler(pool_menu_callbacks, pattern="pool_menu"),
        ],
        states={
            "SELECTING": [CallbackQueryHandler(save_button_input)],
            "TYPING": [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_text_input)
            ],
            "CONFIRM": [CallbackQueryHandler(choose)],
        },
        fallbacks=[CommandHandler("start", home)],
        per_message=False,
        per_user=True,
    )

    schedule_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(schedule_menu_callbacks, pattern="schedule_menu"),
        ],
        states={},
        fallbacks=[CommandHandler("start", home)],
        per_message=False,
        per_user=True,
    )

    application.add_handler(conv_handler)
    application.add_handler(pool_handler)

    application.add_handler(schedule_handler)

    application.add_handler(CallbackQueryHandler(inline_menu))

    # log all errors
    application.add_error_handler(error)

    # Job queue for calling the invitations
    """
    application.job_queue.run_repeating(
        callback=remind,
        interval=timedelta(days=1),
        first=time_until(os.getenv("REMIND_AT")),
    )
    application.job_queue.run_repeating(
        callback=raffle_pairs,
        interval=timedelta(days=1),
        first=time_until(os.getenv("LOTTERY_AT")),
    )
    """
    application.run_polling()


if __name__ == "__main__":
    # init tables
    ACCOUNTS.check_db()
    POOLS.check_db()
    SCHEDULES.check_db()
    POOL_MEMBERS.check_db()

    main()

    print("Shutting the bot down")
    ACCOUNTS.close_connection()
    POOLS.close_connection()
    SCHEDULES.close_connection()
    POOL_MEMBERS.close_connection()
