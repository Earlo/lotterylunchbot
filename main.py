from data.users import Users
from data.pools import Pools
from data.schedules import Schedules

from commands import register_user, count, skip, raffle_pairs, remind, debug_raffle_pairs
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, ChosenInlineResultHandler
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

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
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Job queue for calling the invitations
    j = updater.job_queue
    j.run_repeating(remind, interval=timedelta(
        days=1), first=time_until(os.getenv('REMIND_AT')))
    j.run_repeating(raffle_pairs, interval=timedelta(
        days=1), first=time_until(os.getenv('LOTTERY_AT')))
    # Start the Bot
    updater.start_polling()
    updater.idle()


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
    print(f"time until {clock} is {next_time - now}")
    return 1
    return next_time - now


if __name__ == '__main__':
    # init users
    Users()
    main()
