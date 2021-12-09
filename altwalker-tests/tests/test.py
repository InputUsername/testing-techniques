import random
from dataclasses import dataclass

from .base import *

@dataclass
class User:
    username: str
    password: str
    access_token: str
    id: str


@dataclass
class Room:
    creator: str
    name: str
    is_private: bool
    id: str


class UserAndRoomManagement:
    def setUpModel(self, data):
        self.users = dict()
        data['users_registered'] = 0

        self.logged_in = dict()
        data['users_logged_in'] = 0

        self.rooms = dict()
        data['rooms'] = 0

    def tearDownModel(self, data):
        print(self.users)
        print(self.logged_in)
        print(data)

    def v_start(self, _data):
        pass

    def e_register(self, data):
        username = 'altwalker_user_' + str(random.randint(0, 999_999_999))
        password = 'password123'

        registration_access_token, user_id = register(username, password)

        self.users[username] = User(username, password, registration_access_token, user_id)
        data['users_registered'] = int(data['users_registered']) + 1

    def v_registered(self, data):
        assert int(data['users_registered']) != 0

        for username, _user in self.users.items():
            assert not available(username)

    def e_login(self, data):
        for username, user in self.users.items():
            if username not in self.logged_in:
                access_token = login(username, user.password)
                self.users[username].access_token = access_token
                self.logged_in[username] = user
                data['users_logged_in'] = int(data['users_logged_in']) + 1
                break

    def e_registered_login(self, data):
        for username, user in self.users.items():
            if username not in self.logged_in:
                self.logged_in[username] = user
                data['users_logged_in'] = int(data['users_logged_in']) + 1
                break

    def v_logged_in(self, data):
        assert int(data['users_registered']) != 0
        assert int(data['users_logged_in']) != 0

        for _username, user in self.logged_in.items():
            response = whoami(user.access_token)
            assert response.status_code == 200
            assert response.json()["user_id"] == user.id

    def e_create_room(self, data):
        room_name = 'altwalker_room_' + str(random.randint(0, 999_999_999))
        is_private = bool(random.getrandbits(1))
        user = random.choice(list(self.logged_in.values()))

        room_id = create_room(room_name, is_private, user.access_token)

        self.rooms[room_name] = Room(user.username, room_name, is_private, room_id)
        data['rooms'] = int(data['rooms']) + 1

    def v_room_created(self, data):
        assert int(data['rooms']) != 0

        for _room_name, room in self.rooms.items():
            response = list_room(room.id)
            assert response.status_code == 200
            is_private = response.json()['visibility'] == 'private'
            assert is_private == room.is_private
