from random import shuffle

from singleton import Singleton


class Users(metaclass=Singleton):
    users = {}
    free_users = set()
    def __getitem__(self, i):
        return self.users[i]

    def __setitem__(self, i, value):
        self.users[i] = value

    def __iter__(self):
        for x in self.users:
            yield x

    def __len__(self):
        return len(self.users)

    def get_pairs(self):
        rngkeys = list(self.users.keys())
        shuffle(rngkeys)
        if (len(rngkeys) % 2 == 1):
            rngkeys.append(None)
        pairs = [[rngkeys[x*2],rngkeys[x*2+1]] for x in range(len(rngkeys)//2)]
        print(pairs)
        return pairs