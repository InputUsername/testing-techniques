from base import *

# The client-server API typically uses HTTP PUT to submit requests with a client-generated transaction identifier.
# This means that these requests are idempotent. The scope of a transaction identifier is a particular access token.
# It only serves to identify new requests from retransmits.
# After the request has finished, the {txnId} value should be changed (how is not specified; a monotonically increasing integer is recommended).


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def main():
    token_1, user_1 = register('tc7_user1', 'password123')
    token_2, user_2 = register('tc7_user2', 'password321')

    # User 1 and 2 login
    token_1 = login('tc7_user1', 'password123')
    token_2 = login('tc7_user2', 'password321')

    # User 1 creates a public room
    room_id = create_room('tc7_room', False, token_1)

    # User 2 joins the room
    status_code = join_room(token_2, room_id)
    assert status_code == 200

    # User 2 checks messages
    res3 = get_request("/_matrix/client/r0/sync", token_2)
    prev_value = json_extract(res3.json(), 'prev_batch')

    # User 1 sends same message twice
    body = {"msgtype": "m.text", "body": "test"}
    res = put_request("/_matrix/client/r0/rooms/" + room_id +
                      "/send/m.room.message/m1636570192032.0", body, token_1)
    assert(res.status_code == 200)
    res2 = put_request("/_matrix/client/r0/rooms/" + room_id +
                      "/send/m.room.message/m1636570192032.0", body, token_1)
    assert(res2.status_code == 200)

    res3 = get_request("/_matrix/client/r0/sync", token_2)

    res4 = get_request("/_matrix/client/r0/rooms/" + room_id + "/messages?from=" + prev_value[0], token_2)

    # Assert if there is only 1 message received
    assert(len(res4.json()['chunk']) == 1)


    print('Test case 7 (double messages) successful')


if __name__ == '__main__':
    main()
