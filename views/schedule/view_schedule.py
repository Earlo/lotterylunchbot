from telegram import InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ContextTypes

from constants import DAYS, TIMES


def TIME_KEYBOARD(offset: int, calendar: list, callback_str) -> InlineKeyboardMarkup:
    width = 3
    # Emoji to use when calendar slot is set to true
    emoji = "🟢"
    # Emoji to use when calendar slot is set to true only in some of the calendars. Something yellow
    emoji_partial = "🟡"

    day_grid = [
        [
            InlineKeyboardButton(
                f"{'✅'if calendar[di +  offset][ti] else ''} {d} {t}",
                callback_data=f"{callback_str}:toggle:{di +  offset}-{ti}",
            )
            for di, d in enumerate(DAYS[offset : width + offset])
        ]
        for ti, t in enumerate(TIMES)
    ]
    arrows = []
    if offset > 0:
        arrows.append(
            InlineKeyboardButton(
                "⬅️", callback_data=f"{callback_str}:move:{offset - 1}"
            )
        )
    if offset + width < len(DAYS):
        arrows.append(
            InlineKeyboardButton(
                "➡️", callback_data=f"{callback_str}:move:{offset + 1}"
            )
        )
    day_grid.append(arrows)
    day_grid.append(
        [
            InlineKeyboardButton("Save changes", callback_data=f"{callback_str}:save"),
        ],
    )

    return InlineKeyboardMarkup(day_grid)


SCHEDULE_EDIT_INSTRUCTIONS = (
    """Click on the time slots that work for your lunch schedule\."""
)

POOL_SCHEDULE_EDIT_INSTRUCTIONS = """\n You're editing your schedule for pool *{}*\."""


async def view_schedule(
    reply_method: callable,
    context: ContextTypes.DEFAULT_TYPE,
    callback_str: str = "schedule_menu",
):
    return await reply_method(
        text=SCHEDULE_EDIT_INSTRUCTIONS
        if context.user_data["CALENDER_POOL"] is None
        else SCHEDULE_EDIT_INSTRUCTIONS
        + POOL_SCHEDULE_EDIT_INSTRUCTIONS.format(context.user_data["CALENDER_POOL"]),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        reply_markup=TIME_KEYBOARD(
            context.user_data["MENU_OFFSET"],
            context.user_data["CALENDER"],
            callback_str,
        ),
    )
