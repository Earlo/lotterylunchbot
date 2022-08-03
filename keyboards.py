from array import array
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


def POOLS_KEYBOARD(account: int) -> InlineKeyboardMarkup:
    pool_buttons = list(
        chunks(
            [
                InlineKeyboardButton(
                    f"View {pool['name']}",
                    callback_data=f"pool_menu:{pool['id']}",
                )
                for pool in POOLS.availeable_pools(account)
            ],
            3,
        )
    )
    pool_buttons.append(
        [
            InlineKeyboardButton("Back", callback_data="profile"),
        ]
    )
    return InlineKeyboardMarkup(pool_buttons)


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
                InlineKeyboardButton("Back", callback_data="pool_menu"),
            ],
        ]
    )


SCHEDULE_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Edit schedule", callback_data="schedule_menu:edit"),
        ],
        [
            InlineKeyboardButton("back", callback_data="profile"),
        ],
    ]
)


def TIME_KEYBOARD(offset: int, calendar: array):
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
