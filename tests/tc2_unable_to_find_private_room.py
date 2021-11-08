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
    (access_token_1, _user_id_1) = register("tc2_user1", "privatepassword1A")

    room_name = "tc2_private_room"
    _room_id = create_room(room_name, True, access_token_1)

    public_rooms = find_public_rooms(access_token_1, room_name).json()
    
    assert(public_rooms["total_room_count_estimate"] == 0)

    print("Test case 2 successfull")

if __name__ == "__main__":
    main()
