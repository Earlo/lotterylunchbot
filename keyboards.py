from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from data.pools import POOLS
from data.schedules import DAYS, TIMES
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

CANCEL_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Cancel", callback_data="delete"),
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
            InlineKeyboardButton("Manage schedule", callback_data="schedule_menu"),
        ],
        [InlineKeyboardButton("Close dialog", callback_data="delete")],
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
                text="Return to pool menu",
                callback_data="pool_menu",
            ),
        ],
    ]
)


def POOL_OPTIONS_KEYBOARD(has_pools: bool = False) -> InlineKeyboardMarkup:
    keys = [
        [
            InlineKeyboardButton(
                text="Browse public pools",
                callback_data="pool_menu:browse",
            )
        ],
        [
            InlineKeyboardButton(
                text="Join a private pool",
                callback_data="pool_menu:join",
            )
        ],
        [
            InlineKeyboardButton(
                text="Create a new pool",
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
                    text="Browse your pools",
                    callback_data="pool_menu:manage",
                )
            ],
        )
    return InlineKeyboardMarkup(keys)


def POOLS_KEYBOARD(
    extra: str = "", pools_shown: list = POOLS.public_pools()
) -> InlineKeyboardMarkup:
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
                    "Back",
                    callback_data=return_page
                    if return_page is not None
                    else "pool_menu",
                ),
            ],
        ]
    )


def TIME_KEYBOARD(offset: int, calendar: list):
    width = 3
    day_grid = [
        [
            InlineKeyboardButton(
                f"{'✅'if calendar[di +  offset][ti] else ''} {d} {t}",
                callback_data=f"schedule_menu:toggle:{di +  offset}-{ti}",
            )
            for di, d in enumerate(DAYS[offset : width + offset])
        ]
        for ti, t in enumerate(TIMES)
    ]
    arrows = []
    if offset > 0:
        arrows.append(
            InlineKeyboardButton("⬅️", callback_data=f"schedule_menu:move:{offset - 1}")
        )
    if offset + width < len(DAYS):
        arrows.append(
            InlineKeyboardButton("➡️", callback_data=f"schedule_menu:move:{offset + 1}")
        )
    day_grid.append(arrows)
    day_grid.append(
        [
            InlineKeyboardButton("Save changes", callback_data="schedule_menu:save"),
        ],
    )

    return InlineKeyboardMarkup(day_grid)
