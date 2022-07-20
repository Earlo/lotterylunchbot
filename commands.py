from data.users import Users
from data.pools import Pools
from data.schedules import Schedules

from messages import *
from utils import check_users

from keyboards import HOMEKEYBOARD, OPTIONS_KEYBOARD, POOLS_KEYBOARD, OK_KEYBOARD
from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext
from telegram import ParseMode


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    USERS = Users()
    userid = str(update.message.from_user.id)
    if userid in USERS:
        user = USERS[userid]
        await update.message.reply_text(
            text=GREETING.format(user["first_name"], os.environ.get("LOTTERY_AT")),
            reply_markup=HOMEKEYBOARD,
        )
    else:
        USERS[userid] = update.message.from_user
        await update.message.reply_text(
            text=GREETING_NEW.format(update.message.from_user.first_name),
            reply_markup=HOMEKEYBOARD,
        )


async def skip(update: Update, context: ContextTypes):
    userid = str(update.message.from_user.id)
    if userid in Users():
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
        await context.bot.send_message(
            chat_id=u,
            text=REMINDER.format(os.environ.get("LOTTERY_AT")),
            reply_markup=OK_KEYBOARD,
        )


async def raffle_pairs(context: CallbackContext):
    await check_users(context)
    for a, b in Users().get_pairs():
        if a == None or b == None:
            try:
                await context.bot.send_message(
                    chat_id=a, text=MISS, reply_markup=OK_KEYBOARD
                )
            except:
                await context.bot.send_message(
                    chat_id=b, text=MISS, reply_markup=OK_KEYBOARD
                )
        else:
            await context.bot.send_message(
                chat_id=a, text=LUNCH.format(Users()[b]["username"])
            )
            await context.bot.send_message(
                chat_id=b, text=LUNCH.format(Users()[a]["username"])
            )
    Users().reset()


async def debug_raffle_pairs(update: Update, context: ContextTypes):
    await raffle_pairs(context)


async def inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()
    if query.data == "options":
        return await options_menu(query, update)
    elif query.data == "pools":
        return await pools_menu(query, update)
    elif query.data == "close":
        return await query.delete_message()

    await query.edit_message_text(
        text=f"Selected option: {query.data}", reply_markup=OPTIONS_KEYBOARD
    )


async def options_menu(query: CallbackQuery, update: Update) -> None:
    user = Users()[query.from_user.id]
    await query.edit_message_text(text=f"{user}", reply_markup=OPTIONS_KEYBOARD)


async def pools_menu(query: CallbackQuery, update: Update) -> None:
    await query.edit_message_text(
        text=POOL_OPTIONS.format(query.from_user.first_name),
        reply_markup=POOLS_KEYBOARD(),
        parse_mode=ParseMode.MARKDOWN,
    )
