from person import Person 

from users import Users
from keyboards import keyboards
from messages import GREETING, GREETING_NEW, TALLY, LUNCH

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

def count(update, context):
    update.message.reply_text(
        text=TALLY.format(len(Users()))
    )

def raffle_pairs(context):
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

