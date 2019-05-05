from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from singleton import Singleton
from constants import CUSTOM_FIELDS, CUSTOM_FIELD_OPTIONS

class Keyboards(metaclass=Singleton):
    def __init__(self):
        self.keyboards = {}
        for F in CUSTOM_FIELD_OPTIONS:
            keyboard = []
            for line in CUSTOM_FIELD_OPTIONS[F]:
                keyboard.append([])
                for item in line:
                    keyboard[-1].append(InlineKeyboardButton(item[0], callback_data=item[1]))
            self.keyboards[F] = InlineKeyboardMarkup(keyboard)

    def __getitem__(self, i):
        return self.keyboards[i]

    def __setitem__(self, i, value):
        self.keyboards[i] = value

keyboards = Keyboards()