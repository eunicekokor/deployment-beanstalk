class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, '1@test.com', 'test'),
    User(2, '2@test.com', 'test'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
