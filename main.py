from data.users import Users
from data.pools import Pools
from data.schedules import Schedules

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    JobQueue
)

from commands import register_user, count, skip, raffle_pairs, remind, debug_raffle_pairs, inline_menu
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


async def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    application = Application.builder().token(os.getenv('TOKEN')).build()

    # Get the dispatcher to register handlers
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', register_user),
            CommandHandler('count', count),
            CommandHandler('skip', skip),
            CommandHandler('debugraffle', debug_raffle_pairs),
        ],
        states={},
        fallbacks=[CommandHandler('start', register_user)],
        per_message=False,
        per_user=True
    )
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(inline_menu))
    # log all errors
    application.add_error_handler(error)

    # Job queue for calling the invitations
    application.job_queue.run_repeating(callback=remind, interval=timedelta(
        days=1), first=time_until(os.getenv('REMIND_AT')))
    application.job_queue.run_repeating(callback=raffle_pairs, interval=timedelta(
        days=1), first=time_until(os.getenv('LOTTERY_AT')))
    # Start the Bot
    application.run_polling()


def time_until(clock: str):
    """
    clock: HH:MM
    Returns the amount of time it takes until it's the clock time.
    """
    h, m = clock.split(":")
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    next_time = tomorrow.hour < int(h) and now.replace(hour=int(h), minute=int(
        m), second=0, microsecond=0) or tomorrow.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
    print(
        f"time until {clock} is {next_time - now}, {(next_time - now) / 3000}")
    return (next_time - now) / 3000
    return next_time - now


if __name__ == '__main__':
    # init users
    Users()
    main()
