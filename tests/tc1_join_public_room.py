from base import *

def main():
    access_token = login("marnick", "marnickssecret123")

    print(create_room("piet", False, access_token))
    print(register("ties8", "hello1234jaja"))
    print(login("marnick", "marnickssecret123"))


if __name__ == "__main__":
    main()
