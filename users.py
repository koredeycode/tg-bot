import json
from datetime import datetime


class User():
    is_bot: bool
    first_name: str
    id: int
    username: str

    def __init__(self, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                self.__dict__[k] = v
        else:
            self.is_bot = True
            self.first_name = ""
            self.id = None
            self.username = ""
            self.point = 0
            self.refferals = 0
        # self.__dict__['created'] = datetime.now()
        # self.__dict__['updated'] = datetime.now()

    def to_dict(self):
        return self.__dict__

    def save(self):
        with open('db.json', 'r') as f:
            users = json.load(f)
            users.append(self.to_dict())
            print(users)
        with open("db.json", 'w') as f:
            json.dump(users, f)
