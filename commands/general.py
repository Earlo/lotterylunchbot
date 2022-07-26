from data.users import USERS

from messages import *
from utils import check_users

from keyboards import HOMEKEYBOARD, OPTIONS_KEYBOARD, POOLS_KEYBOARD, OK_KEYBOARD
from telegram import Update, CallbackQuery, constants
from telegram.ext import ContextTypes, CallbackContext
from telegram.helpers import escape_markdown


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userid = str(update.message.from_user.id)
    if userid in USERS:
        user = USERS[userid]
        await update.message.reply_text(
            text=escape_markdown(
                GREETING.format(user["first_name"], os.environ.get("LOTTERY_AT")),
                version=2,
            ),
            reply_markup=HOMEKEYBOARD,
        )
    else:
        USERS[userid] = update.message.from_user
        await update.message.reply_text(
            text=escape_markdown(
                GREETING_NEW.format(update.message.from_user.first_name), version=2
            ),
            reply_markup=HOMEKEYBOARD,
        )


async def skip(update: Update, context: ContextTypes):
    userid = str(update.message.from_user.id)
    if userid in USERS:
        USERS.disqualified_users.add(userid)
    else:
        # user not registered, register first, then skip today
        register_user(update, context)
        skip(update, context)


async def count(update: Update, context: ContextTypes):
    await check_users(context)
    await update.message.reply_text(
        text=escape_markdown(TALLY.format(len(USERS)), version=2)
    )


async def remind(context: CallbackContext):
    await check_users(context)
    for u in USERS:
        await context.bot.send_message(
            chat_id=u,
            text=escape_markdown(
                REMINDER.format(os.environ.get("LOTTERY_AT")), version=2
            ),
            reply_markup=OK_KEYBOARD,
        )


async def raffle_pairs(context: CallbackContext):
    await check_users(context)
    for a, b in USERS.get_pairs():
        if a == None or b == None:
            try:
                await context.bot.send_message(
                    chat_id=a,
                    text=escape_markdown(MISS, version=2),
                    reply_markup=OK_KEYBOARD,
                )

            except:
                await context.bot.send_message(
                    chat_id=b,
                    text=escape_markdown(MISS, version=2),
                    reply_markup=OK_KEYBOARD,
                )

        else:
            await context.bot.send_message(
                chat_id=a,
                text=escape_markdown(LUNCH.format(USERS[b]["username"]), version=2),
            )

            await context.bot.send_message(
                chat_id=b,
                text=escape_markdown(LUNCH.format(USERS[a]["username"]), version=2),
            )

    USERS.reset()


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
        text=escape_markdown(f"Selected option: {query.data}", version=2),
        reply_markup=OPTIONS_KEYBOARD,
    )


async def options_menu(query: CallbackQuery, update: Update) -> None:
    user = USERS[query.from_user.id]
    await query.edit_message_text(
        text=escape_markdown(f"{user}", version=2), reply_markup=OPTIONS_KEYBOARD
    )


async def pools_menu(query: CallbackQuery, update: Update) -> None:
    await query.edit_message_text(
        text=escape_markdown(
            POOL_OPTIONS.format(query.from_user.first_name), version=2
        ),
        reply_markup=POOLS_KEYBOARD(),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
