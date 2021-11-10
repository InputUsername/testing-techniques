from base import *

"""
9.6.1   PUT /_matrix/client/r0/rooms/{roomId}/state/{eventType}/{stateKey}
"""
def change_room_alias(access_token, room_id, room_alias):
    body = {
        "alt_aliases": [room_id]
    }

    response = put_request(
        "/_matrix/client/r0/rooms/" + room_id + "/state/m.room.canonical_alias", body, access_token)

    return response.status_code


def main():
    # [Precondition]: create test user 1
    (access_token_1, _user_id_1) = register("tc13_user1", "privatepassword1A")

    # [Precondition]: create public test room
    room_id = create_room("tc13_public_room", False, access_token_1)

    # Execute the test case and assert the (expected) post condition
    assert(change_room_alias(access_token_1, room_id, "SomeInvalidAddress") == 400)

    print("Test case 13 (publish nonexistent local address) successfull")


if __name__ == "__main__":
    main()
