import os

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from commands.utils import get_times_string, get_user_schedule, requires_account
from data.accounts import ACCOUNTS
from data.pools import POOLS
from data.schedules import DAYS
from keyboards import OK_KEYBOARD, OPTIONS_KEYBOARD
from messages import *
from utils import check_accounts


@requires_account
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await profile_menu(update, context)


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
    await check_accounts(context)
    for a, b in ACCOUNTS.get_pairs():
        if a == None or b == None:
            try:
                await context.bot.send_message(
                    chat_id=a,
                    text=MISS,
                    reply_markup=OK_KEYBOARD,
                )
            except:
                await context.bot.send_message(
                    chat_id=b,
                    text=MISS,
                    reply_markup=OK_KEYBOARD,
                )
        else:
            await context.bot.send_message(
                chat_id=a,
                text=LUNCH.format(escape_markdown(ACCOUNTS[b]["username"], version=2)),
            )
            await context.bot.send_message(
                chat_id=b,
                text=LUNCH.format(escape_markdown(ACCOUNTS[a]["username"], version=2)),
            )
    ACCOUNTS.reset()


async def debug_raffle_pairs(update: Update, context: ContextTypes):
    await raffle_pairs(context)


async def inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    selected = options[0]
    if "CALENDER" not in context.user_data:
        get_user_schedule(update.effective_user.id, context)

    if selected == "delete":
        return await query.delete_message()
    elif selected == "profile":
        return await send_profile_menu(query.edit_message_text, context)
    await query.edit_message_text(
        text=f"""View not implemented yet\.
        Selected option: {query.data}
        While state is {context.chat_data.get("state")}
        You should not see this message. :D please make a bug report at the project's github page.""",
        reply_markup=OPTIONS_KEYBOARD,
    )
    return -1


async def profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_profile_menu(update.message.reply_text, context)


async def send_profile_menu(reply, context: ContextTypes.DEFAULT_TYPE):
    account = ACCOUNTS[context._user_id]
    pools_in = POOLS.pools_in(context._user_id)

    filtered_days = list(
        filter(lambda column: True in column, context.user_data.get("CALENDER", []))
    )
    account_schedule = [
        SCHEDULE_MENU_DATE_LINE.format(
            DAYS[day_index],
            get_times_string(column),
        )
        for day_index, column in enumerate(filtered_days)
    ]
    account_pools = [
        POOL_LIST.format(
            "🌐" if p["public"] else "🔐",
            escape_markdown(p["name"], version=2),
            f"{p['member_count']} members" if p["member_count"] > 1 else "Just you 😔",
        )
        for p in pools_in
    ]
    if account_schedule == []:
        account_schedule = [NO_SCHEDULE_SET]
    if account_pools == []:
        account_pools = [NO_POOLS_JOINED]

    await reply(
        text=OPTIONS.format(
            escape_markdown(account["first_name"], version=2),
            "\n".join(account_pools),
            "\n".join(account_schedule),
        ),
        reply_markup=OPTIONS_KEYBOARD,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
