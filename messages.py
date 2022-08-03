GREETING_NEW = """Hello {}\!
You seem to be a new user\!
You are now part of upcoming lunch lotteries\.
"""

GREETING = """Hello {}\!
Lunch Lottery is conducted every day at {}\."""

TALLY = """There are {} people using this bot\!"""

REMINDER = """Lunch Lottery is conducted at {}\.
If you don't want to take part to the next lunch pairing, use `\/skip`\."""

LUNCH = """Today you'll be having lunch with @{}\!
Send them a message\!"""

MISS = """Sorry, you were the odd one out today and we couldn't find you a lunch partner :("""


OPTIONS = """Hello *{}*,
__You are in lottery pools:__
{}

__You're availeable for lunch on:__
{}
"""

POOL_EXPLANATION = """The lunch lotteries are conducted in among the pool members\.

Here you can manage the pools you are a member of, and join new ones\.

You can also create your own pool\.
"""


POOL_LIST = """{} *{}* has {}\."""

POOL_BROWSE_PUBLIC = """Click on the pools below to view them\."""

POOL_DESCRIPTION = """*{}*
_{} _

Public: {}

Members: {}
{}
"""


CREATE_POOL0 = """Hello *{}*,

Please enter the name of your pool\.
"""

CREATE_POOL1 = """Set name to *{}*,

Do you want your pool to be public or private?"""

CREATE_POOL2 = """Do you want to add a description?"""

CREATE_POOL3 = """Please type your pool's description\."""


CREATE_POOL4 = """Creating pool\. 

Name: {}
Description: {}
Public: {}"""


CREATE_POOL5 = """Created pool\. 

Name: {}
Description: {}
Public: {}"""

EDIT_POOL_DONE = """Edited pool\. 

Name: {}
Description: {}
Public: {}"""


JOIN_POOL_PROMT = """Enter the pool's name you want to join\."""

JOIN_POOL_FAIL = """Pool named _{} _doesn't exist\."""

JOIN_POOL_ALREADY_MEMBER = """You are already a member of _{}\._"""

JOIN_POOL_SUCCESS = """You have joined pool _{}\._"""


LEAVE_POOL_FAIL = """Pool named _{} _doesn't exist\."""

LEAVE_POOL_NOT_MEMBER = """You are not a member of _{}\._"""

LEAVE_POOL_SUCCESS = """You have left pool _{}\._"""

POOL_EDIT = """Please enter the new {} of your pool\."""


SCHEDULE_MENU = """Schedule for *{}*,
```
{}
```
"""

SCHEDULE_MENU_DATE_LINE = """{}: {}"""

SCHEDULE_EDIT_INSTRUCTIONS = (
    """Click on the time slots that work for your lunch schedule\."""
)

NO_SCHEDULE_SET = """You haven't set a schedule yet\.
You need to have a schedule before you can participate in lunch lotteries\.

Click 'Manage schedule' to set one\.
"""

NO_POOLS_JOINED = """You haven't joined any pools yet\.
You need to be a member of a pool before you can participate in lunch lotteries\.

Click 'Manage pools' to join or create one\.
"""
