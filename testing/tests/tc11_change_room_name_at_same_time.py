from base import *

import threading

"""
9.6.1   PUT /_matrix/client/r0/rooms/{roomId}/state/{eventType}/{stateKey}
"""
def set_room_name(access_token, room_id, name):
    body = {
        "name": name
    }

    response = put_request("/_matrix/client/r0/rooms/" + room_id +
                           "/state/m.room.name/", body, access_token)

    return response.status_code

class ChangeRoomTester(threading.Thread):
    def __init__(self, access_token, room_id, name):
        threading.Thread.__init__(self)

        self.access_token = access_token
        self.room_id = room_id
        self.name = name

    def run(self):
        assert(set_room_name(self.access_token, self.room_id, self.name) == 200)

def main():
    # [Precondition]: create test users 1 and 2
    (access_token, _user_id) = register("tc11_user", "privatepassword1A")

    # [Precondition]: create public test room
    room_id = create_room("tc11_public_room", False, access_token)

    threads = []

    t1 = ChangeRoomTester(access_token, room_id, "t1roomnamechange")
    t2 = ChangeRoomTester(access_token, room_id, "t2roomnamechange")

    # Execute the test case and assert the (expected) post condition
    t1.start()
    t2.start()

    threads.append(t1)
    threads.append(t2)

    for t in threads:
        t.join()

    print("Test case 11 (change room name at the same time) successful")

if __name__ == "__main__":
    main()
