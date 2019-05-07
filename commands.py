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
        Users()[userid] = user
        update.message.reply_text(
            text=GREETING_NEW.format(user.first_name)
        )

def skip(update, context):
    userid = update.message.from_user.id
    if (userid in Users()):
        Users().disqualified_users.add(userid)
    else:
        # User not registered
        pass


def count(update, context):
    update.message.reply_text(
        text=TALLY.format(len(Users()))
    )

def remind(context):
    check_users(context)
    for u in Users():
        context.bot.send_message(chat_id=u,
            text=REMINDER)

def raffle_pairs(context):
    check_users(context)
    for a, b in Users().get_pairs():
        if (a == None or b == None):
            try:
                context.bot.send_message(chat_id=a,
                    text='Sorry, you were the odd one out today :(')
            except:
                context.bot.send_message(chat_id=b,
                    text='Sorry, you were the odd one out today :(')
        else:
            context.bot.send_message(chat_id=a, 
                text=LUNCH.format(Users()[b].username))
            context.bot.send_message(chat_id=b, 
                text=LUNCH.format(Users()[a].username))

def check_users(context):
    to_delete = set()
    for u in Users():
        try:
            context.bot.send_chat_action(u, 'typing')
        except Exception as e:
            print(e)
            to_delete.add(u)
    for u in to_delete:
        del Users()[u]

