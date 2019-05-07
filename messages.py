from constants import LOTTERY_AT

GREETING_NEW = """Hello {}!
You seem to be a new user!
Hope you find nice people to lunch with.
"""

GREETING = """Hello {{}}!
Lunch Lottery is conducted every day at {}.""".format(LOTTERY_AT)

TALLY ="""There are {} people using this bot!"""

REMINDER="""Lunch Lottery is conducted at {}.
If you don't want to take part today, use /skip""".format(LOTTERY_AT)

LUNCH ="""Today you'll be having lunch with @{}!
Send them a message!"""