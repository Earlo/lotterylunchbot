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
            InlineKeyboardButton("Manage pools", callback_data="pool_menu"),
            InlineKeyboardButton("Manage dates", callback_data="date_menu"),
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
                    f"View {pool['name']}", callback_data=f"pool_menu:{pool['id']}"
                )
                for pool in POOLS.public_pools()
            ],
            [
                InlineKeyboardButton("Back", callback_data="profile"),
            ],
        ]
    )


def POOL_KEYBOARD(pool: dict, is_member: bool, is_admin: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{'Leave' if is_member else 'Join'} {pool['name']}",
                    callback_data=f"pool_menu:{pool['id']}:{'leave' if is_member else 'join'}",
                )
            ],
            [
                InlineKeyboardButton(
                    f"Edit name",
                    callback_data=f"pool_menu:{pool['id']}:edit:name",
                ),
                InlineKeyboardButton(
                    f"Edit description",
                    callback_data=f"pool_menu:{pool['id']}:edit:description",
                ),
                InlineKeyboardButton(
                    f"Make {'private' if pool['public'] else 'public'}",
                    callback_data=f"pool_menu:{pool['id']}:edit:public:{not pool['public']}",
                ),
            ]
            if is_admin
            else [],
            [
                InlineKeyboardButton("Back", callback_data="ools_menu"),
            ],
        ]
    )
