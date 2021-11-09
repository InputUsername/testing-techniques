from base import *


"""
10.4.3.3   POST /_matrix/client/r0/rooms/{roomId}/kick
"""
def kick(access_token, room_id, user_id, reason):
    body = {
        "user_id": user_id,
        "reason": reason
    }

    response = post_request("/_matrix/client/r0/rooms/" +
                            room_id + "/kick", body, access_token)

    return response.status_code


def main():
    token_1, user_1 = register('tc6_user1', 'password123')
    token_2, user_2 = register('tc6_user2', 'password321')

    # User 1 and 2 login
    token_1 = login('tc6_user1', 'password123')
    token_2 = login('tc6_user2', 'password321')

    # User 1 creates a public room
    room_id = create_room('tc4_room', False, token_1)

    # User 2 joins the room
    status_code = join_room(token_2, room_id)
    assert status_code == 200

    # User 1 kicks user 2 from the room
    status_code = kick(token_1, room_id, user_2, 'You have been kicked')
    assert status_code == 200

    # User 2 can rejoin the room
    status_code = join_room(token_2, room_id)
    assert status_code == 200

    print('Test case 6 (kicked user can rejoin room) successful')


if __name__ == '__main__':
    main()
