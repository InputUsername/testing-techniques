import random
import string
from datetime import datetime
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
    messages: list


@dataclass
class Message:
    msg: str
    event_id: str
    sender: str

    def __repr__(self):
        max_len = min(20, len(self.msg))
        snippet = self.msg[:max_len]
        return f'Message(msg=\'{snippet}...\', event_id=\'{self.event_id}\', sender=\'{self.sender}\')'


users = dict()
logged_in = dict()
rooms = dict()


class UserAndRoomManagement:
    """
    Models user and room management in Matrix by randomly registering users,
    logging them in, creating rooms, and letting users join rooms.
    """

    def setUpModel(self, data):
        """
        Called on model creation.
        """

        data['users_registered'] = 0
        data['users_logged_in'] = 0
        data['rooms'] = 0
        data['max_room_members'] = 0
        data['possible_joins'] = 0

    def tearDownModel(self, data):
        """
        Called on model destruction.
        """

        print('\n'.join(str(user) for user in users.values()), end='\n\n')
        print(','.join(str(user.username) for user in logged_in.values()), end='\n\n')
        print('\n'.join(str(room) for room in rooms.values()), end='\n\n')
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

        username = 'altwalker_user_' + str(datetime.now().strftime('%s')) + str(random.randint(0, 999_999_999))
        password = 'password123'

        registration_access_token, user_id = register(username, password)

        users[username] = User(username, password, registration_access_token, user_id)
        data['users_registered'] = len(users)

    def v_registered(self, data):
        """
        Called when v_registered is visited.
        This asserts that the corresponding username is not available anymore,
        ie. that the user has been registered.
        """

        assert int(data['users_registered']) != 0

        for username, _user in users.items():
            assert not available(username)

        # print(data)

    def e_login(self, data):
        """
        Called when e_login is followed.
        Logs a user in using the dedicated Matrix API endpoint.
        """

        for username, user in users.items():
            if username not in logged_in:
                access_token = login(username, user.password)
                users[username].access_token = access_token
                logged_in[username] = user
                data['users_logged_in'] = len(logged_in)
                break

    def v_logged_in(self, data):
        """
        Called when v_login is visited.
        This asserts that every user in the model actually exists.
        """

        assert int(data['users_logged_in']) != 0

        for _username, user in logged_in.items():
            response = whoami(user.access_token)
            assert response.status_code == 200
            assert response.json()["user_id"] == user.id

    def e_create_room(self, data):
        """
        Called when e_create_room is followed.
        Creates a room in Matrix and in the model.
        """

        room_name = 'altwalker_room_' + str(datetime.now().strftime('%s')) + str(random.randint(0, 999_999_999))
        is_private = bool(random.getrandbits(1))
        user = random.choice(list(logged_in.values()))

        room_id = create_room(room_name, is_private, user.access_token)

        rooms[room_name] = Room(user.username, room_name, is_private, room_id, set(), list())
        data['rooms'] = len(rooms)

    def v_room_created(self, data):
        """
        Called when v_room_created is visited.
        This asserts that every room in the model actually exists
        and has the right properties (access rights).
        """

        assert int(data['rooms']) != 0

        possible_joins = 0

        for _room_name, room in rooms.items():
            response = list_room(room.id)
            assert response.status_code == 200
            is_private = response.json()['visibility'] == 'private'
            assert is_private == room.is_private

            for username, _user in logged_in.items():
                # print('=======================')
                # print(username, 'CHECKING JOINABILITY OF', _room_name)
                # print(room.creator, room.members, room.is_private)

                if username not in room.members:
                    if (not room.is_private) or username == room.creator:
                        # print('COULD JOIN!!')

                        possible_joins += 1

        data['possible_joins'] = possible_joins

        # print('\n'.join(str(room) for room in rooms.values()))
        # print(data)


    def e_join_room(self, data):
        """
        Called when e_join_room is followed.
        This causes a user that is not yet a member of the room to join it.
        """

        for _room_name, room in rooms.items():
            for username, user in logged_in.items():
                if username not in room.members:
                    if (not room.is_private) or username == room.creator:
                        status_code = join_room(user.access_token, room.id)
                        assert status_code == 200
                        room.members.add(username)
                        return

        raise Exception('unexpected: e_join_room did not join a room')

    def v_room_joined(self, data):
        """
        Called when v_room_joined is visited.
        Asserts that the room membership status in the model matches that
        in Matrix itself.
        """

        for _room_name, room in rooms.items():
            data['max_room_members'] = max(int(data['max_room_members']), len(room.members))

        assert(int(data['max_room_members']) != 0)

        for username, user in users.items():
            user_rooms = set(joined_rooms(user.access_token)['joined_rooms'])

            for _room_name, room in rooms.items():
                # If a user is in a room according to the model,
                # the room should be in the list of joined rooms for that user.
                if username in room.members:
                    assert room.id in user_rooms


class Messaging:
    def setUpModel(self, data):
        self.messaging_rooms = dict()

        self.txn_id = 0

        data['room_has_messages'] = False

    def tearDownModel(self, data):
        print('\n'.join(str(room) for room in self.messaging_rooms.values()))

    def retrieve_messages(self, access_token, room_id):
        response = sync(access_token)

        assert response.status_code == 200

        messages = []

        room_data = response.json()['rooms']['join'][room_id]

        for event in room_data['timeline']['events']:
            if event['type'] == 'm.room.message' and 'body' in event['content']:
                username = next(username for username, user in logged_in.items() if user.id == event['sender'])
                msg = Message(event['content']['body'], event['event_id'], username)
                messages.append(msg)

        return messages

    def v_in_room(self, data):
        room_has_messages = False

        for room_name, room in rooms.items():
            if len(room.members) != 0:
                self.messaging_rooms[room_name] = room

            if len(room.messages) != 0:
                room_has_messages = True

        data['room_has_messages'] = room_has_messages

        for _room_name, room in self.messaging_rooms.items():
            # Pick a member to retrieve room state for
            user = logged_in[next(iter(room.members))]

            room_messages = self.retrieve_messages(user.access_token, room.id)

            # if room_messages != room.messages:
            #     print('actual:')
            #     print('\n'.join(str(msg) for msg in room_messages), end='\n\n')
            #     print('expected:')
            #     print('\n'.join(str(msg) for msg in room.messages))

            assert room_messages == room.messages


    def e_send_message(self, data):
        room = random.choice(list(self.messaging_rooms.values()))
        username = random.choice(list(room.members))
        user = logged_in[username]

        message_length = random.randint(1, 30)
        message = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(message_length))

        response = send_message(user.access_token, room.id, self.txn_id, message)

        assert response.status_code == 200

        event_id = response.json()['event_id']

        # print(room.name, '\nbefore send =======================')
        # print('\n'.join(str(msg) for msg in room.messages))

        room.messages.append(Message(message, event_id, user.username))

        # print('after send =======================')
        # print('\n'.join(str(msg) for msg in room.messages))

        self.txn_id += 1

    def e_redact_message(self, data):
        room = random.choice(list(self.messaging_rooms.values()))
        while len(room.messages) == 0:
            room = random.choice(list(self.messaging_rooms.values()))

        msg_idx = random.randint(0, len(room.messages) - 1)
        message = room.messages[msg_idx]
        user = logged_in[message.sender]

        response = redact(user.access_token, room.id, self.txn_id, message.event_id)

        assert response.status_code == 200

        # print(room.name, '\nbefore redact =======================')
        # print('\n'.join(str(msg) for msg in room.messages))

        room.messages.remove(message)

        # print('after redact =======================')
        # print('\n'.join(str(msg) for msg in room.messages))

        self.txn_id += 1
