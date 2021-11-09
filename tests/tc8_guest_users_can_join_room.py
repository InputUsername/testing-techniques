from base import *

def main():
    # [Precondition]: create test users 1 and 2
    guest_username = "tc8_guest_user"

    (access_token_1, _user_id_1) = register("tc8_user", "privatepassword1A")
    (access_token_2, _user_id_2) = register(guest_username, "privatepassword1B", True)

    # [Precondition]: create public test room
    room_id = create_room("tc8_public_room", True, access_token_1)

    # Execute the test case and assert the (expected) post condition
    assert(join_room(access_token_2, room_id) == 200)

    print("Test case 8 (guest user can join room) successfull")

if __name__ == "__main__":
    main()
