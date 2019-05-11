from person import Person 

from users import Users
from keyboards import keyboards
from messages import *

def start(update, context):
    userid = update.message.from_user.id
    if (userid in Users()):
        user = Users()[userid]
        update.message.reply_text(
            text=GREETING.format(user.first_name)
        )
    else:
        user = Person(update.message.from_user)
        if (len(user.username) > 0):
            Users()[userid] = user
            print("New user", user.username)
            update.message.reply_text(
                text=GREETING_NEW.format(user.first_name)
            )
        else:
            update.message.reply_text(
                text='You need username to use this bot'
            )


def skip(update, context):
    userid = update.message.from_user.id
    if (userid in Users()):
        Users().disqualified_users.add(userid)
    else:
        # user not registered, register first, then skip today
        start(update, context)
        skip(update, context)


def count(update, context):
    check_users(context)
    update.message.reply_text(text=TALLY.format(len(Users())))

def remind(context):
    check_users(context)
    for u in Users():
        context.bot.send_message(chat_id=u,
            text=REMINDER)

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
                text=LUNCH.format(Users()[b].username))
            context.bot.send_message(chat_id=b, 
                text=LUNCH.format(Users()[a].username))
    Users().reset()

def check_users(context):
    to_delete = set()
    for u in Users():
        try:
            context.bot.send_chat_action(u, 'typing')
            Users()[u].update_data(context.bot.getChat(u))
        except:
            to_delete.add(u)
    for u in to_delete:
        print("Removing", Users()[u].username)
        del Users()[u]

