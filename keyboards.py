from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data.pools import POOLS

CLEANUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🧹", callback_data="delete"),
        ],
    ]
)

OK_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Ok", callback_data="delete"),
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
            InlineKeyboardButton("Manage pools", callback_data="pools_menu"),
            InlineKeyboardButton("Manage dates", callback_data="dates_menu"),
        ],
        [InlineKeyboardButton("Back", callback_data="0")],
    ]
)

YES_NO_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Yes",
                callback_data="True",
            ),
            InlineKeyboardButton(
                text="No",
                callback_data="False",
            ),
        ]
    ]
)

SUBMIT_CANCEL_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Submit",
                callback_data="True",
            ),
            InlineKeyboardButton(
                text="Cancel",
                callback_data="False",
            ),
        ]
    ]
)


def POOLS_KEYBOARD() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    pool["name"], callback_data=f"pool_menu:{pool['id']}"
                )
                for pool in POOLS.public_pools()
            ],
            [
                InlineKeyboardButton("Back", callback_data="profile"),
            ],
        ]
    )
