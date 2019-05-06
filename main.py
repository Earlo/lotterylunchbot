#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import requests
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, ChosenInlineResultHandler

from constants import TOKEN 
from commands import * 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def statehandler(bot, update):
    print("State is being handled uwu")

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
    j.run_repeating(raffle_pairs, interval=1, first=0)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
