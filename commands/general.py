import os

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from commands.pool import pools_menu
from commands.utils import get_times_string, get_user_schedule, requires_account
from data.accounts import ACCOUNTS
from data.poolMembers import POOL_MEMBERS
from data.pools import POOLS
from data.schedules import DAYS, TIMES
from keyboards import AWAY_KEYBOARD, OK_KEYBOARD, OPTIONS_KEYBOARD
from messages import *
from utils import check_accounts


@requires_account
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await profile_menu(update, context)
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
    for di, d in enumerate(DAYS):
        for ti, i in enumerate(TIMES):
            pairs = POOL_MEMBERS.get_pairs(ti, di)
            print(d, i, pairs)
    """
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
    """


async def debug_raffle_pairs(update: Update, context: ContextTypes):
    await raffle_pairs(context)


async def meta_inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    selected = options[0]
    if "CALENDER" not in context.user_data:
        get_user_schedule(update.effective_user.id, context)
    if selected == "delete":
        await query.delete_message()
    elif selected == "profile":
        await send_profile_menu(query.edit_message_text, context)
    elif selected == "cancel":
        # I don't like this, but egh
        if options[1] == "pool_menu":
            await pools_menu(query, update)
    elif selected == "account_menu":
        if options[1] == "toggle":
            if options[2] == "disqualified":
                ACCOUNTS.set_disqualified(
                    update.effective_user.id, options[3] == "True"
                )
        await send_profile_menu(query.edit_message_text, context)
    else:
        await query.edit_message_text(
            text=f"""View not implemented yet\.
            Selected option: {query.data}
            You should not see this message. :D please make a bug report at the project's github page.""",
            reply_markup=OPTIONS_KEYBOARD,
        )
    return -1


async def profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_profile_menu(update.message.reply_text, context)


async def send_profile_menu(reply, context: ContextTypes.DEFAULT_TYPE):
    account = ACCOUNTS[context._user_id]
    pools_in = POOLS.pools_in(context._user_id)

    account_schedule = [
        SCHEDULE_MENU_DATE_LINE.format(
            DAYS[day_index],
            get_times_string(column),
        )
        for day_index, column in enumerate(context.user_data.get("CALENDER", []))
    ]

    account_schedule = list(
        filter(lambda sched: "No times selected" not in sched, account_schedule)
    )
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

    if account["disqualified"]:
        await reply(
            text=OPTIONS_AWAY.format(escape_markdown(account["first_name"], version=2)),
            reply_markup=AWAY_KEYBOARD,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    else:
        await reply(
            text=OPTIONS.format(
                escape_markdown(account["first_name"], version=2),
                "\n".join(account_pools),
                "\n".join(account_schedule),
            ),
            reply_markup=OPTIONS_KEYBOARD,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
