from base import *

def main():
    # [Precondition]: create test users 1 and 2
    (access_token_1, _user_id_1) = register("tc1_user1", "privatepassword1A")
    (access_token_2, _user_id_2) = register("tc1_user2", "privatepassword1B")

    # [Precondition]: create public test room
    room_id = create_room("tc1_public_room", False, access_token_1)

    # Execute the test case and assert the (expected) post condition
    assert(join_room(access_token_2, room_id) == 200)

    print("Test case 1 (join public room) successfull")

if __name__ == "__main__":
    main()
