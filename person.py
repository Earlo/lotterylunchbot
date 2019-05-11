from constants import CUSTOM_FIELDS

class Person:
    def __init__(self, user):
        self.data = {'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'username': user.username}

    @property
    def id(self):
        return self.data['id']
    
    @property
    def first_name(self):
        return self.data['first_name']
    
    @property
    def last_name(self):
        return self.data['last_name']
    
    @property
    def username(self):
        return self.data['username']
    
    def __eq__(self, other):
        if(isinstance(other, Person)):
            return other.id == self.id
        else:
            return False

    def update_data(self, data):
        self.data = {'id': data['id'], 
                'first_name': data['first_name'], 
                'last_name': data['last_name'], 
                'username': data['username']}
