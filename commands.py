from data.users import Users
from data.pools import Pools
from data.schedules import Schedules

from messages import *
from utils import check_users

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    USERS = Users()
    userid = str(update.message.from_user.id)
    if (userid in USERS):
        user = USERS[userid]
        await update.message.reply_text(
            text=GREETING.format(user['first_name'],
                                 os.environ.get("LOTTERY_AT")),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        USERS[userid] = update.message.from_user
        await update.message.reply_text(
            text=GREETING_NEW.format(update.message.from_user.first_name),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def skip(update: Update, context: ContextTypes):
    userid = str(update.message.from_user.id)
    if (userid in Users()):
        Users().disqualified_users.add(userid)
    else:
        # user not registered, register first, then skip today
        register_user(update, context)
        skip(update, context)


async def count(update: Update, context: ContextTypes):
    await check_users(context)
    update.message.reply_text(text=TALLY.format(len(Users())))


async def remind(context: CallbackContext):
    await check_users(context)
    for u in Users():
        await context.bot.send_message(chat_id=u,
                                       text=REMINDER.format(os.environ.get("LOTTERY_AT")))


async def raffle_pairs(context: CallbackContext):
    await check_users(context)
    for a, b in Users().get_pairs():
        print("doing", a, b)
        if (a == None or b == None):
            try:
                await context.bot.send_message(chat_id=a, text=MISS)
            except:
                await context.bot.send_message(chat_id=b, text=MISS)
        else:
            await context.bot.send_message(chat_id=a,
                                           text=LUNCH.format(Users()[b]['username']))
            await context.bot.send_message(chat_id=b,
                                           text=LUNCH.format(Users()[a]['username']))
    Users().reset()


async def debug_raffle_pairs(update: Update, context: ContextTypes):
    await raffle_pairs(context)


async def inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
