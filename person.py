from constants import CUSTOM_FIELDS

class Person:
    def __init__(self, User):
        self.User = User
        self.custom_fields = {}
        for c in CUSTOM_FIELDS:
            self.custom_fields[c] = ""

    @property
    def id(self):
        return self.User.id
    
    @property
    def first_name(self):
        return self.User.first_name
    
    @property
    def last_name(self):
        return self.User.last_name
    
    @property
    def username(self):
        return self.User.username
    
    def __eq__(self, other):
        if(isinstance(other, Person)):
            return other.id == self.id
        else:
            return False