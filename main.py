from data.users import Users

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands.general import (
    register_user,
    count,
    skip,
    raffle_pairs,
    remind,
    debug_raffle_pairs,
    inline_menu,
)
from commands.pool import create_pool, pool_creation_form
from commands.utils import save_input

from utils import time_until
from datetime import timedelta
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


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
            CommandHandler("start", register_user),
            CommandHandler("count", count),
            CommandHandler("skip", skip),
            CommandHandler("debugraffle", debug_raffle_pairs),
        ],
        states={},
        fallbacks=[CommandHandler("start", register_user)],
        per_message=False,
        per_user=True,
    )

    # Get the dispatcher to register handlers
    pool_handler = ConversationHandler(
        entry_points=[
            CommandHandler("create_pool", create_pool),
        ],
        states={
            "SELECTING": [CallbackQueryHandler(pool_creation_form)],
            "TYPING": [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
        },
        fallbacks=[CommandHandler("start", register_user)],
        per_message=False,
        per_user=True,
    )

    application.add_handler(conv_handler)
    application.add_handler(pool_handler)

    application.add_handler(CallbackQueryHandler(inline_menu))

    # log all errors
    application.add_error_handler(error)

    # Job queue for calling the invitations
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
    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    # init users
    Users()
    main()
