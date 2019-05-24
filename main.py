#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import requests
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, ChosenInlineResultHandler

from datetime import datetime, timedelta, time

from constants import TOKEN, REMIND_AT, LOTTERY_AT, TIMEZONE
from commands import start, count, skip, raffle_pairs, remind, debug_raffle_pairs

from users import Users

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"', bot, update.error)

def main():
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('count', count),
            CommandHandler('skip', skip),
            CommandHandler('debugraffle', debug_raffle_pairs),
        ],
        states={},
        fallbacks=[CommandHandler('start', start)],
        per_message=False,
        per_user=True
    )
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    
    # Job queue for calling the invitations
    j = updater.job_queue
    j.run_repeating(remind, interval=timedelta(days=1), first=time_until(REMIND_AT)) 
    j.run_repeating(raffle_pairs, interval=timedelta(days=1), first=time_until(LOTTERY_AT))

    # Start the Bot
    updater.start_polling()

    updater.idle()

def time_until(t):
    h, m = t.split(":")
    dt = datetime.now()
    tomorrow = dt + timedelta(days=1)
    t = datetime.combine(tomorrow, time.min) - dt + timedelta(hours=int(h) + TIMEZONE,  minutes=int(m))
    print("Time until first", t)
    return t

if __name__ == '__main__':
    #init users
    Users()
    main()
