from base import *

import threading

no_conflict = False
conflict = False

"""
        PUT /_matrix/client/r0/directory/room/{roomAlias}
"""
def change_room_alias(access_token, room_id, room_alias):
    body = {
        "room_id": room_id
    }

    response = put_request(
        "/_matrix/client/r0/directory/room/" + room_alias, body, access_token)

    return response.status_code


class IdenticalAddressTester(threading.Thread):
    def __init__(self, access_token, room_id):
        threading.Thread.__init__(self)

        self.access_token = access_token
        self.room_id = room_id
        self.address = "%23identicalalias:my.matrix.host"

    def run(self):
        global no_conflict
        global conflict

        result = change_room_alias(self.access_token, self.room_id, self.address)

        if result == 200:
            no_conflict = True

        if result == 409:
            conflict = True


def main():
    # [Precondition]: create test users 1 and 2
    (access_token_1, _user_id_1) = register("tc10_user_1", "privatepassword1A")
    (access_token_2, _user_id_2) = register("tc10_user_2", "privatepassword1A")

    # [Precondition]: create public test room
    room_id_1 = create_room("tc10_public_room_1", False, access_token_1)
    room_id_2 = create_room("tc10_public_room_2", False, access_token_2)

    threads = []

    t1 = IdenticalAddressTester(access_token_1, room_id_1)
    t2 = IdenticalAddressTester(access_token_2, room_id_2)

    # Execute the test case and assert the (expected) post condition
    t1.start()
    t2.start()

    threads.append(t1)
    threads.append(t2)

    for t in threads:
        t.join()

    assert (conflict and no_conflict)

    print("Test case 10 (two identical addresses at the same time) successfull")


if __name__ == "__main__":
    main()
