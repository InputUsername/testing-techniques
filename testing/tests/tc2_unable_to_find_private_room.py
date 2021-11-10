from base import *

"""
10.5.3   GET /_matrix/client/r0/publicRooms

Tries to retrieve the public rooms on the home server.
"""
def find_public_rooms(access_token, filter_keyword):
    body = {
        "filter": {
            "generic_search_term": filter_keyword
        }
    }

    return post_request("/_matrix/client/r0/publicRooms", body, access_token)

def main():
    # [Precondition]: create test user 1
    (access_token_1, _user_id_1) = register("tc2_user1", "privatepassword1A")

    # [Precondition]: create private test room
    room_name = "tc2_private_room"
    _room_id = create_room(room_name, True, access_token_1)

    # Execute the test case
    public_rooms = find_public_rooms(access_token_1, room_name).json()
    
    # Assert the (expected) post condition
    assert(len(public_rooms["chunk"]) == 0)

    print("Test case 2 (unable to find private room) successfull")

if __name__ == "__main__":
    main()
