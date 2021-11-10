from base import *

import threading

sync = threading.Lock()

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
        self.address = "%23identicalalias:synapse"

    def run(self):
        if sync.locked():
            assert(change_room_alias(self.access_token,
                   self.room_id, self.address) == 400)
        else:
            sync.acquire()
            assert(change_room_alias(self.access_token,
                   self.room_id, self.address) == 200)


def main():
    # [Precondition]: create test users 1 and 2
    (access_token_1, _user_id_1) = register("tc10_user", "privatepassword1A")
    (access_token_2, _user_id_2) = register("tc10_user", "privatepassword1A")

    # [Precondition]: create public test room
    room_id_1 = create_room("tc10_public_room", False, access_token_1)
    room_id_2 = create_room("tc10_public_room", False, access_token_2)

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

    print("Test case 10 (two identical addresses at the same time) successfull")


if __name__ == "__main__":
    main()
