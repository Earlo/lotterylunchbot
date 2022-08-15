from telegram import constants
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from commands.utils import get_times_string
from constants import DAYS
from data.accounts import ACCOUNTS
from data.pools import POOLS
from keyboards import AWAY_KEYBOARD, OPTIONS_KEYBOARD

SCHEDULE_MENU_DATE_LINE = """{}: {}"""
POOL_LIST = """{} *{}* has {}\."""
NO_SCHEDULE_SET = """Mon: \-
Tue: \-
Wed: \-
Thu: \-
Fri: \-
Sat: \-
Sun: \-"""

NO_POOLS_JOINED = """\-

Please join at least one group to participate in lunch lotteries\."""

OPTIONS_AWAY = """Hello *{}*,
You're not currently taking part in lottery lunches due to having set your status as *away*\."""

OPTIONS = """Hello *{}*,
__You are in lottery groups:__
{}

__You're availeable for lunch on:__
{}"""


async def view_profile(reply, context: ContextTypes.DEFAULT_TYPE):
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
