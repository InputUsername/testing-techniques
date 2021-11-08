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

    (access_token_1, _user_id_1) = register("tc1_user1", "privatepassword1A")
    (_access_token_2, user_id_2) = register("tc1_user2", "privatepassword1B")

    room_id = create_room("tc1_public_room", False, access_token_1)

    assert(invite(access_token_1, user_id_2, room_id) == 200)

    print("Test case 1 successfull")


if __name__ == "__main__":
    main()
