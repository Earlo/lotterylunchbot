import os
import random
from datetime import datetime

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from commands.pool import pools_menu
from commands.utils import get_times_string, requires_account
from constants import DAYS
from data.accounts import ACCOUNTS
from data.logs import LOGS
from data.poolMembers import POOL_MEMBERS
from data.schedules import SCHEDULES
from keyboards import OK_KEYBOARD, OPTIONS_KEYBOARD
from messages import *
from utils import check_accounts
from views.profile.view_profile import view_profile


@requires_account
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await view_profile(update.message.reply_text, context)
    return -1


@requires_account
async def skip(update: Update, context: ContextTypes):
    ACCOUNTS.disqualified_accounts.add(update.message.from_user.id)


async def remind(context: CallbackContext):
    await check_accounts(context)
    for u in ACCOUNTS:
        await context.bot.send_message(
            chat_id=u,
            text=REMINDER.format(os.environ.get("LOTTERY_AT")),
            reply_markup=OK_KEYBOARD,
        )


async def raffle_pairs(context: CallbackContext):
    # await check_accounts(context)
    # Add one because postgres starts at 1
    matched = set()
    day = datetime.now().weekday() + 1
    print("day is", day)
    pairs = POOL_MEMBERS.get_pairs(day)
    random.shuffle(pairs)
    pairs_messaged = []
    # TODO check that the user is still subscribed before this
    for pair in pairs:
        account_a = pair["a_account"]
        account_b = pair["b_account"]
        if account_a in matched or account_b in matched:
            print("alrayd matched")
        else:
            matched.add(account_a)
            matched.add(account_b)
            group = escape_markdown(pair["pool_name"], version=2)
            times = get_times_string([t == "t" for t in pair["calendar_match"]])
            try:
                await context.bot.send_message(
                    chat_id=account_a,
                    text=LUNCH.format(
                        escape_markdown(pair["b_username"], version=2), group, times
                    ),
                    parse_mode=constants.ParseMode.MARKDOWN_V2,
                )
            except Exception as e:
                print(e)
                print(f"most likley account_a {account_a} has unsubscribed")
                break
            try:
                await context.bot.send_message(
                    chat_id=account_b,
                    text=LUNCH.format(
                        escape_markdown(pair["a_username"], version=2), group, times
                    ),
                    parse_mode=constants.ParseMode.MARKDOWN_V2,
                )
            except Exception as e:
                print(e)
                print(f"most likley account_b {account_b} has unsubscribed")
                break
            pairs_messaged.append(pair)
    LOGS.add_entry(pairs_messaged)


async def debug_raffle_pairs(update: Update, context: ContextTypes):
    if os.environ.get("PRODUCTION") == "False" and update.effective_user.id == int(
        os.environ.get("ADMIN_ACCOUNT_ID")
    ):
        # await raffle_pairs(context)
        for di, d in enumerate(DAYS):
            pairs = POOL_MEMBERS.get_pairs(di + 1)
            print(di + 1, d)
            for pair in pairs:
                print(
                    pair["a_username"],
                    pair["b_username"],
                    pair["pool_name"],
                    pair["calendar_match"],
                    get_times_string([t == "t" for t in pair["calendar_match"]]),
                )


async def debug_announce(update: Update, context: ContextTypes):
    if update.effective_user.id == int(os.environ.get("ADMIN_ACCOUNT_ID")):
        text = " ".join(update.message.text.split(" ")[1:])
        print(text)
        for account in ACCOUNTS:
            try:
                await context.bot.send_message(
                    chat_id=account,
                    text=escape_markdown(text, version=2),
                    parse_mode=constants.ParseMode.MARKDOWN_V2,
                )
            except Exception as e:
                print(e)
                print(f"most likley {account} has unsubscribed")
    else:
        print(update.effective_user.id, " tried to announce:", update.message.text)


async def meta_inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    print(options)
    selected = options[0]
    if "CALENDER" not in context.user_data:
        schedules = SCHEDULES.get_schedule(update.effective_user.id)
        context.user_data["CALENDER"] = schedules["calendar"]
    if selected == "delete":
        return await query.delete_message()
    elif selected == "cancel":
        # I don't like this, but egh
        if options[1] == "pool_menu":
            return await pools_menu(query, update)
    elif selected == "account_menu":
        if options[1] == "toggle":
            if options[2] == "disqualified":
                ACCOUNTS.set_disqualified(
                    update.effective_user.id, options[3] == "True"
                )
    return await view_profile(query.edit_message_text, context)
    '''        
    else:
        await query.edit_message_text(
            text=f"""View not implemented yet\.
            Selected option: {query.data}
            You should not see this message. :D please make a bug report at the project's github page.""",
            reply_markup=OPTIONS_KEYBOARD,
        )
    '''
