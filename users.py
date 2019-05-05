from singleton import Singleton
class Users(metaclass=Singleton):
    users = {}
    def __getitem__(self, i):
        return self.users[i]

    def __setitem__(self, i, value):
        self.users[i] = value

    def __iter__(self):
        for x in self.users:
            yield x

users = Users()

