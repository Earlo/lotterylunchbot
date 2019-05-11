from random import shuffle

from singleton import Singleton

import json

class Users(metaclass=Singleton):
    users = {}
    disqualified_users = set()
    def __init__(self):
        self.load()

    def __getitem__(self, i):
        return self.users[i]

    def __setitem__(self, i, data):
        try:
            value = {'id': data.id, 
            'first_name': data.first_name, 
            'last_name': data.last_name, 
            'username': data.username}
        except AttributeError:
            value.data = {'id': data['id'], 
                'first_name': data['first_name'], 
                'last_name': data['last_name'], 
                'username': data['username']}
        self.users[i] = value

    def __iter__(self):
        for x in self.users:
            yield x

    def __len__(self):
        return len(self.users)

    def __delitem__(self, key):
        del self.users[key]

    def __repr__(self):
        return self.users.__repr__()

    def get_qualified(self):
        return list(set(self.users.keys()).difference(self.disqualified_users))

    def get_pairs(self):
        rngkeys = self.get_qualified()
        shuffle(rngkeys)
        if (len(rngkeys) % 2 == 1):
            rngkeys.append(None)
        pairs = [[rngkeys[x*2],rngkeys[x*2+1]] for x in range(len(rngkeys)//2)]
        print(pairs)
        return pairs
    
    def reset(self):
        self.disqualified_users = set()

    def save(self):
        with open('users.json', 'w') as fp:
            json.dump(self.users, fp)

    def load(self):
        print("LOADING")
        with open('users.json', 'r') as fp:
            self.users = json.load(fp)
