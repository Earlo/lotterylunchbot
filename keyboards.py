from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import chunks

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

POOL_CANCEL_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Cancel", callback_data="cancel:pool_menu"),
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
            InlineKeyboardButton("Manage groups", callback_data="pool_menu"),
            InlineKeyboardButton("Manage schedule", callback_data="schedule_menu"),
        ],
        [
            InlineKeyboardButton(
                "Take a break", callback_data="account_menu:toggle:disqualified:True"
            )
        ],
    ]
)

AWAY_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Return from the break",
                callback_data="account_menu:toggle:disqualified:False",
            )
        ],
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
RETURN_TO_POOL_MENU_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Return to group menu",
                callback_data="pool_menu",
            ),
        ],
    ]
)


def POOL_OPTIONS_KEYBOARD(has_pools: bool = False) -> InlineKeyboardMarkup:
    keys = [
        [
            InlineKeyboardButton(
                text="Browse public groups",
                callback_data="pool_menu:browse",
            )
        ],
        [
            InlineKeyboardButton(
                text="Join a private group",
                callback_data="pool_menu:join",
            )
        ],
        [
            InlineKeyboardButton(
                text="Create a new group",
                callback_data="pool_menu:create",
            )
        ],
        [
            InlineKeyboardButton(
                text="Go back",
                callback_data="profile",
            )
        ],
    ]
    if has_pools:
        keys.insert(
            0,
            [
                InlineKeyboardButton(
                    text="Browse your groups",
                    callback_data="pool_menu:manage",
                )
            ],
        )
    return InlineKeyboardMarkup(keys)


def POOLS_KEYBOARD(extra: str = "", pools_shown: list = []) -> InlineKeyboardMarkup:
    pool_buttons = list(
        chunks(
            [
                InlineKeyboardButton(
                    f"View {pool['name']}",
                    callback_data=f"pool_menu:{pool['id']}:view{extra}",
                )
                for pool in pools_shown
            ],
            3,
        )
    )
    pool_buttons.append(
        [
            InlineKeyboardButton("Back", callback_data="pool_menu"),
        ]
    )
    return InlineKeyboardMarkup(pool_buttons)


def POOL_KEYBOARD(
    pool: dict, is_member: bool, is_admin: bool, return_page: str | None = None
) -> InlineKeyboardMarkup:
    print("doing ppol keyboartd", pool, is_member, is_admin, return_page)
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
                    callback_data=f"pool_menu:{pool['id']}:toggle:public:{not pool['public']}",
                ),
            ]
            if is_admin
            else [],
            [
                InlineKeyboardButton(
                    f"🆘 Delete {pool['name']} 🆘",
                    callback_data=f"pool_menu:{pool['id']}:delete",
                ),
            ]
            if is_admin
            else [],
            [
                InlineKeyboardButton(
                    f"Set your schedule for {pool['name']}",
                    callback_data=f"pool_menu:{pool['id']}:schedule",
                )
            ]
            if is_member
            else [],
            [
                InlineKeyboardButton(
                    "Back",
                    callback_data=return_page
                    if return_page is not None
                    else "pool_menu",
                ),
            ],
        ]
    )
