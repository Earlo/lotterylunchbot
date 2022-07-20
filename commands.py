from data.users import Users
from data.pools import Pools
from data.schedules import Schedules

from messages import *


def register_user(update, context):
    USERS = Users()
    userid = str(update.message.from_user.id)
    print(userid, "in", USERS)
    if (userid in USERS):
        user = USERS[userid]
        update.message.reply_text(
            text=GREETING.format(user['first_name'],
                                 os.environ.get("LOTTERY_AT"))
        )
    else:
        USERS[userid] = update.message.from_user
        update.message.reply_text(
            text=GREETING_NEW.format(update.message.from_user.first_name)
        )


def skip(update, context):
    userid = str(update.message.from_user.id)
    if (userid in Users()):
        Users().disqualified_users.add(userid)
    else:
        # user not registered, register first, then skip today
        register_user(update, context)
        skip(update, context)


def count(update, context):
    check_users(context)
    update.message.reply_text(text=TALLY.format(len(Users())))


def remind(context):
    check_users(context)
    for u in Users():
        context.bot.send_message(chat_id=u,
                                 text=REMINDER.format(os.environ.get("LOTTERY_AT")))


def debug_raffle_pairs(update, context):
    raffle_pairs(context)


def raffle_pairs(context):
    check_users(context)
    for a, b in Users().get_pairs():
        if (a == None or b == None):
            try:
                context.bot.send_message(chat_id=a, text=MISS)
            except:
                context.bot.send_message(chat_id=b, text=MISS)
        else:
            context.bot.send_message(chat_id=a,
                                     text=LUNCH.format(Users()[b]['username']))
            context.bot.send_message(chat_id=b,
                                     text=LUNCH.format(Users()[a]['username']))
    Users().reset()


def check_users(context):
    to_delete = set()
    for u in Users():
        try:
            context.bot.send_chat_action(u, 'typing')
            Users()[u] = context.bot.getChat(u)
        except:
            to_delete.add(u)
    for u in to_delete:
        print("Removing", Users()[u]['username'])
        del Users()[u]
    Users().save()
