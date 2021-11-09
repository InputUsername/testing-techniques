from base import *

"""
10.4.2.1   POST /_matrix/client/r0/rooms/{roomId}/invite

Tries to invite the given user id to the given room id and returns the HTTP response code.
"""
def invite(access_token, user_id, room_id):
    body = {
        "user_id": user_id
    }

    response = post_request("/_matrix/client/r0/rooms/" +
                            room_id + "/invite", body, access_token)

    return response.status_code

def main():
    # [Precondition]: create test users 1 and 2
    (access_token_1, _user_id_1) = register("tc3_user1", "privatepassword1A")
    (access_token_2, user_id_2) = register("tc3_user2", "privatepassword1B")

    # [Precondition]: create private test room
    room_id = create_room("tc1_public_room", True, access_token_1)

    # Execute the test case and assert the (expected) post condition
    assert(invite(access_token_1, user_id_2, room_id) == 200)

    print("Test case 3 (invite user to private room) successfull")


if __name__ == "__main__":
    main()
