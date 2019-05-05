from person import Person 

from users import users
from keyboards import keyboards

def start(update, context):
    userid = update.message.from_user.id
    if (userid in users):
        user = users[userid]
        update.message.reply_text(
            text="You are already using lotterylunchbot"
        )
    else:
        user = Person(update.message.from_user)
        users[userid] = user
        update.message.reply_text(
            text="You seem to be a new user!\nPlease fill this basic information."
        )
    update.message.reply_text('Please choose:', reply_markup=keyboards["HOME"])
    return "SCHOOL"

def startMenu(update, context):
    user = users[update.callback_query.message.chat.id]
    query = update.callback_query
    return query.data

def setSchool(update, context):
    user = users[update.callback_query.message.chat.id]
    query = update.callback_query

    user.custom_fields["SCHOOL"] = query.data
    query.edit_message_text(text="Selected school: {}".format(user.custom_fields["SCHOOL"]),
    reply_markup=keyboards[query.data])

    return "FIELD"

def setField(update, context):
    user = users[update.callback_query.message.chat.id]
    query = update.callback_query

    user.custom_fields["FIELD"] = query.data
    query.edit_message_text(text="Selected school: {}\nSelected field: {}".format(
        user.custom_fields["SCHOOL"],user.custom_fields["FIELD"]))

    return "TARGET"

def setTarget(update, context):
    user = users[update.callback_query.message.chat.id]
    query = update.callback_query

    user.custom_fields["FIELD"] = query.data
    query.edit_message_text(text="Selected school: {}\nSelected field: {}".format(
        user.custom_fields["SCHOOL"],user.custom_fields["FIELD"]))

    return "HOME"
