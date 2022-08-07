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
__You are in lottery groups:__
{}

__You're availeable for lunch on:__
{}
"""

OPTIONS_AWAY = """Hello *{}*,
You're not currently taking part in lottery lunches due to having set your status as *away*\."""


POOL_EXPLANATION = """The lunch lotteries are conducted in among the group members\.

Here you can manage the groups you are a member of, and join new ones\.

You can also create your own group\.
"""


POOL_LIST = """{} *{}* has {}\."""

POOL_BROWSE_PUBLIC = """Click on the groups below to view them\."""

POOL_DESCRIPTION = """*{}*
_{} _

Public: {}

Members: {}
{}
"""


CREATE_POOL0 = """Let's create you a new lottery lunch group\!,

Please enter the name of your group\.
"""

CREATE_POOL1 = """Set name to *{}*,

Do you want your group to be public or private?"""

CREATE_POOL2 = """Do you want to add a description?"""

CREATE_POOL3 = """Please type your group's description\."""


CREATE_POOL4 = """Creating group\. 

Name: {}
Description: {}
Public: {}"""

CREATE_POOL_CANCEL = """Group creation cancelled\."""

JOIN_POOL_PROMT = """Enter the group's name you want to join\."""

JOIN_POOL_FAIL = """Group named _{} _doesn't exist\."""

JOIN_POOL_ALREADY_MEMBER = """You are already a member of _{}\._"""

JOIN_POOL_SUCCESS = """You have joined group _{}\._"""


LEAVE_POOL_FAIL = """Group named _{} _doesn't exist\."""

LEAVE_POOL_NOT_MEMBER = """You are not a member of _{}\._"""

LEAVE_POOL_SUCCESS = """You have left group _{}\._"""

POOL_EDIT = """Please enter the new {} of your group\."""

POOL_EDIT_CONFIRM = """change {} {} to {}?"""

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

NO_POOLS_JOINED = """You haven't joined any groups yet\.
You need to be a member of a group before you can participate in lunch lotteries\.

Click 'Manage groups' to join or create one\.
"""
