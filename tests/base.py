import requests

"""
5.5.2   POST /_matrix/client/r0/login

Attempts to login a user in and returns the access token.
"""
def login(username, password):
    body = {
        "type": "m.login.password",
        "identifier": {
            "type": "m.id.user",
            "user": username
        },
        "password": password
    }

    return post_request("/_matrix/client/r0/login", body).json()["access_token"]


"""
5.6.1   POST /_matrix/client/r0/register

Attempts to register a user and returns the access token and user id.
"""
def register(username, password, is_guest=False):
    kind = "user"

    if is_guest:
        kind = "guest"

    #  _______________________
    # |       Stage 0         |
    # | No auth               |
    # |  ___________________  |
    # | |_Request_1_________| | <-- Returns "session" key which is used throughout.
    # |_______________________|

    session = post_request(
        "/_matrix/client/r0/register?kind=" + kind, {}).json()["session"]

    body = {
        "auth": {
            "type": "m.login.dummy",
            "session": session
        },
        "username": username,
        "password": password
    }

    #  _______________________
    # |       Stage 1         |
    # | type: "<auth type1>"  |
    # |  ___________________  |
    # | |_Request_1_________| |
    # |_______________________|

    response = post_request("/_matrix/client/r0/register?kind=user", body).json()

    return (response["access_token"], response["user_id"])


"""
10.1.1   POST /_matrix/client/r0/createRoom

Attempts to create a room and returns the room id.
"""
def create_room(name, is_private, access_token):
    visibility = "public"

    if is_private:
        visibility = "private"

    body = {
        "visibility": visibility,
        "name": name
    }

    return post_request("/_matrix/client/r0/createRoom", body, access_token).json()["room_id"]


"""
10.4.2.2   POST /_matrix/client/r0/rooms/{roomId}/join
"""
def join_room(access_token, room_id):
    response = post_request("/_matrix/client/r0/rooms/" + room_id + "/join", {}, access_token)

    return response.status_code

"""
Execute a POST request towards the local matrix server with an optional access token.
"""
def post_request(endpoint, body, access_token=None):
    headers_dict = dict()

    if access_token:
        headers_dict["Authorization"] = "Bearer " + access_token

    return requests.post("http://localhost:8008" + endpoint,
                         headers=headers_dict,
                         json=body
                         )

"""
Execute a GET request towards the local matrix server with an optional access token.
"""
def get_request(endpoint, access_token=None):
    headers_dict = dict()

    if access_token:
        headers_dict["Authorization"] = "Bearer " + access_token

    return requests.get("http://localhost:8008" + endpoint, headers=headers_dict)