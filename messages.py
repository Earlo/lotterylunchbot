from constants import LOTTERY_AT

GREETING_NEW = """Hello {}!
You seem to be a new user!
You are now part of upcoming lunch lotteries.
"""

GREETING = """Hello {{}}!
Lunch Lottery is conducted every day at {}.""".format(LOTTERY_AT)

TALLY = """There are {} people using this bot!"""

REMINDER = """Lunch Lottery is conducted at {}.
If you don't want to take part to the next lunch pairing, use /skip""".format(LOTTERY_AT)

LUNCH = """Today you'll be having lunch with @{}!
Send them a message!"""

MISS = """Sorry, you were the odd one out today :("""