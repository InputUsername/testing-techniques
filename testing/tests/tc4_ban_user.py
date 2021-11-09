from base import *

"""
10.4.4.1   POST /_matrix/client/r0/rooms/{roomId}/ban
"""
def ban(access_token, user_id, room_id, reason):
    body = {
        "user_id": user_id,
        "reason": reason
    }

    response = post_request("/_matrix/client/r0/rooms/" +
                            room_id + "/ban", body, access_token)

    return response.status_code


def main():
    token_1, user_1 = register('tc4_user1', 'password123')
    token_2, user_2 = register('tc4_user2', 'password321')

    # User 1 and 2 login
    token_1 = login('tc4_user1', 'password123')
    token_2 = login('tc4_user2', 'password321')

    # User 1 creates a public room
    room_id = create_room('tc4_room', False, token_1)

    # User 2 joins the room
    status_code = join_room(token_2, room_id)
    assert status_code == 200

    # User 1 bans user 2; this also kicks user 2 from the room
    status_code = ban(token_1, user_2, room_id, 'You have been banned')
    assert status_code == 200

    print('Test case 4 (ban user) successful')


if __name__ == '__main__':
    main()
