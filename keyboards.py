from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data.pools import Pools

OK_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Ok", callback_data="close"),
        ],
    ]
)


HOMEKEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Profile", callback_data="profile"),
            InlineKeyboardButton("Check next lunch raffle", callback_data="schedule"),
        ],
    ]
)

OPTIONS_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Manage pools", callback_data="pools"),
            InlineKeyboardButton("Manage dates", callback_data="dates"),
        ],
        [InlineKeyboardButton("Back", callback_data="0")],
    ]
)


def POOLS_KEYBOARD() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(pool.name) for pool in Pools().public_pools()]]
    )
