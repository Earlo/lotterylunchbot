from multiprocessing import context
import os
from telegram import Update, CallbackQuery, constants
from telegram.ext import ContextTypes, CallbackContext
from telegram.helpers import escape_markdown

from data.accounts import ACCOUNTS
from data.pools import POOLS

from messages import *
from utils import check_accounts
from keyboards import HOMEKEYBOARD, OPTIONS_KEYBOARD, POOLS_KEYBOARD, OK_KEYBOARD
from commands.utils import requires_account


@requires_account
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    account = ACCOUNTS[update.message.from_user.id]
    await update.message.reply_markdown_v2(
        text=GREETING.format(
            escape_markdown(account["first_name"], version=2),
            os.environ.get("LOTTERY_AT"),
        ),
        reply_markup=HOMEKEYBOARD,
    )


@requires_account
async def skip(update: Update, context: ContextTypes):
    ACCOUNTS.disqualified_accounts.add(update.message.from_user.id)


async def count(update: Update, context: ContextTypes):
    await check_accounts(context)
    await update.message.reply_markdown_v2(
        text=TALLY.format(len(ACCOUNTS)),
    )


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
    selected = query.data.split(":")[0]
    if selected == "profile":
        return await profile_menu(query, update)
    elif selected == "pools_menu":
        return await pools_menu(query, update)
    elif selected == "pool_menu":
        return await pool_menu(query, update, pool_id=query.data.split(":")[1])
    elif selected == "delete":
        return await query.delete_message()

    await query.edit_message_text(
        text=f"Selected option: {query.data}",
        reply_markup=OPTIONS_KEYBOARD,
    )


async def profile_menu(query: CallbackQuery, update: Update) -> None:
    account = ACCOUNTS[query.from_user.id]
    pools_in = POOLS.pools_in(account["id"])
    await query.edit_message_text(
        text=OPTIONS.format(
            account["first_name"],
            escape_markdown(
                "\n".join(
                    [
                        POOL_LIST.format(
                            "🌐" if p["public"] else "🔐",
                            p["name"],
                            f"{p['count']} members."
                            if p["count"] > 1
                            else "Just you 😔",
                        )
                        for p in pools_in
                    ]
                ),
                version=2,
            ),
            "WIP",
        ),
        reply_markup=OPTIONS_KEYBOARD,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )


async def pools_menu(query: CallbackQuery, update: Update) -> None:
    await query.edit_message_text(
        text=POOL_OPTIONS.format(
            escape_markdown(query.from_user.first_name, version=2)
        ),
        reply_markup=POOLS_KEYBOARD(),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )


async def pool_menu(query: CallbackQuery, update: Update, pool_id: int) -> None:
    pool = POOLS[pool_id]
    await query.edit_message_text(
        text=POOL_DESCRIPTION.format(
            escape_markdown(pool["name"], version=2),
            escape_markdown(pool["description"], version=2),
            "The group is public\." if pool["public"] else "The group is private\.",
            pool["member_count"],
            "You're the admin" if pool["admin"] == query.from_user.id else "",
        ),
        reply_markup=POOLS_KEYBOARD(),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
