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
    members: set


class UserAndRoomManagement:
    """
    Models user and room management in Matrix by randomly registering users,
    logging them in, creating rooms, and letting users join rooms.
    """

    def setUpModel(self, data):
        """
        Called on model creation.
        """

        self.users = dict()
        data['users_registered'] = 0

        self.logged_in = dict()
        data['users_logged_in'] = 0

        self.rooms = dict()
        data['rooms'] = 0
        data['max_room_members'] = 0
        data['joinable_rooms'] = 0

    def tearDownModel(self, data):
        """
        Called on model destruction.
        """

        print(self.users, end='\n\n')
        print(self.logged_in, end='\n\n')
        print(self.rooms, end='\n\n')
        print(data)

    def v_start(self, _data):
        """
        Called when the start state is visited.
        This does nothing.
        """

        pass

    def e_register(self, data):
        """
        Called when e_register is followed.
        Creates a user in Matrix and in the model.
        """

        username = 'altwalker_user_' + str(random.randint(0, 999_999_999))
        password = 'password123'

        registration_access_token, user_id = register(username, password)

        self.users[username] = User(username, password, registration_access_token, user_id)
        data['users_registered'] = int(data['users_registered']) + 1

    def v_registered(self, data):
        """
        Called when v_registered is visited.
        This asserts that the corresponding username is not available anymore,
        ie. that the user has been registered.
        """

        assert int(data['users_registered']) != 0

        for username, _user in self.users.items():
            assert not available(username)

    def e_login(self, data):
        """
        Called when e_login is followed.
        Logs a user in using the dedicated Matrix API endpoint.
        """

        for username, user in self.users.items():
            if username not in self.logged_in:
                access_token = login(username, user.password)
                self.users[username].access_token = access_token
                self.logged_in[username] = user
                data['users_logged_in'] = int(data['users_logged_in']) + 1
                break

    def e_registered_login(self, data):
        """
        Called when e_registered_login is followed.
        On registration, Matrix already returns an access token,
        so effectively the user is logged in. We model this by
        an edge that does nothing except update the login status in the model.
        """

        for username, user in self.users.items():
            if username not in self.logged_in:
                self.logged_in[username] = user
                data['users_logged_in'] = int(data['users_logged_in']) + 1
                break

    def v_logged_in(self, data):
        """
        Called when v_login is visited.
        This asserts that every user in the model actually exists.
        """

        assert int(data['users_registered']) != 0
        assert int(data['users_logged_in']) != 0

        for _username, user in self.logged_in.items():
            response = whoami(user.access_token)
            assert response.status_code == 200
            assert response.json()["user_id"] == user.id

    def e_create_room(self, data):
        """
        Called when e_create_room is followed.
        Creates a room in Matrix and in the model.
        """

        room_name = 'altwalker_room_' + str(random.randint(0, 999_999_999))
        is_private = bool(random.getrandbits(1))
        user = random.choice(list(self.logged_in.values()))

        room_id = create_room(room_name, is_private, user.access_token)

        self.rooms[room_name] = Room(user.username, room_name, is_private, room_id, set())
        data['rooms'] = int(data['rooms']) + 1

    def v_room_created(self, data):
        """
        Called when v_room_created is visited.
        This asserts that every room in the model actually exists
        and has the right properties (access rights).
        """

        assert int(data['rooms']) != 0

        joinable_rooms = 0

        for _room_name, room in self.rooms.items():
            response = list_room(room.id)
            assert response.status_code == 200
            is_private = response.json()['visibility'] == 'private'
            assert is_private == room.is_private

            for username, _user in self.users.items():
                if not room.is_private and username != room.creator and username not in room.members:
                    joinable_rooms += 1

        data['joinable_rooms'] = joinable_rooms


    def e_join_room(self, data):
        """
        Called when e_join_room is followed.
        This causes a user that is not yet a member of the room to join it.
        (Only public rooms can be joined.)
        """

        for _room_name, room in self.rooms.items():
            if room.is_private:
                continue

            for username, user in self.logged_in.items():
                if username != room.creator and username not in room.members:
                    status_code = join_room(user.access_token, room.id)
                    assert status_code == 200
                    room.members.add(username)
                    return

    def e_creator_join(self, data):
        """
        Called when e_creator_join is followed.
        Similar to user creation returning a login token, when a user creates
        a room they also join that room. We model this by an edge that does
        nothing except update the room creator's member status in the model.
        """

        for _room_name, room in self.rooms.items():
            for username, user in self.logged_in.items():
                if username == room.creator:
                    room.members.add(username)
                    return

    def v_room_joined(self, data):
        """
        Called when v_room_joined is visited.
        Asserts that the room membership status in the model matches that
        in Matrix itself.
        """

        for _room_name, room in self.rooms.items():
            data['max_room_members'] = max(int(data['max_room_members']), len(room.members))

        assert(int(data['max_room_members']) != 0)

        for username, user in self.users.items():
            user_rooms = set(joined_rooms(user.access_token)['joined_rooms'])

            for _room_name, room in self.rooms.items():
                # If a user is in a room according to the model,
                # the room should be in the list of joined rooms for that user.
                if username in room.members:
                    assert room.id in user_rooms
