from base import *

"""
9.6.1   PUT /_matrix/client/r0/rooms/{roomId}/state/{eventType}/{stateKey}
"""
def set_guest_access_disabled(access_token, room_id):
    body = {
        "guest_access": "forbidden"
    }

    response = put_request("/_matrix/client/r0/rooms/" + room_id +
                           "/state/m.room.guest_access/", body, access_token)

    return response.status_code

def main():
    # [Precondition]: create test users 1 and 2
    guest_username = "tc9_guest_user"

    (access_token_1, _user_id_1) = register("tc9_user", "privatepassword1A")
    (access_token_2, _user_id_2) = register_guest(
        guest_username, "privatepassword1B")

    # [Precondition]: create private test room
    room_id = create_room("tc9_public_room", False, access_token_1)

    # Execute the test case and assert the (expected) post conditions
    assert(set_guest_access_disabled(access_token_1, room_id) == 200)
    assert(join_room(access_token_2, room_id) == 403)

    print("Test case 9 (guest user cannot join guest access disabled room) successful")


if __name__ == "__main__":
    main()
