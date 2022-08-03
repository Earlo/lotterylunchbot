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
You are in lottery pools: 
{}

You're availeable for lunch on:
{}
"""

POOL_LIST = """{} *{}* has {}\."""

POOL_OPTIONS = """Hello *{}*,
Here are the public pools\.

If you've been asked to join a private pool, use 
`\/join <pool_name>`

To create a new pool use
`\/create_pool`
"""

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
