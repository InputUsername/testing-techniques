import socket
from enum import Enum

"""
Matrix requests types supported by this adapter.

Following the endpoints as described at https://matrix.org/docs/spec/client_server/r0.6.1
"""
class MatrixRequests(Enum):
    # 5.6.1   POST /_matrix/client/r0/register?kind=user
    REGISTER = 'register'

    # 5.5.2   POST /_matrix/client/r0/login
    LOGIN = 'login'

    # 10.1.1   POST /_matrix/client/r0/createRoom
    CREATE_ROOM = 'create_room'


"""
Process a TorXakis request into a Matrix request.

[<request_type> <authentication_type> <optional_authentication_token> <request_body_arguments>]
"""
def process(message: str, sockfile):
    segments = message.split()
    if len(segments) <= 0:
        print('Received empty message')
    else:
        request_identifier = segments[0]
        try:
            request = MatrixRequests(request_identifier)

            match request:
                case MatrixRequests.REGISTER:
                    print("REGISTER")
                    sockfile.write("200\n")
                    sockfile.flush()
                case MatrixRequests.LOGIN:
                    print("LOGIN")
                case MatrixRequests.CREATE_ROOM:
                    print("CREATE ROOM")
        except ValueError as e:
            print(f"Unknown request '{request_identifier}'")


def main():
    with socket.create_server(('', 7890)) as server:
        sock, addr = server.accept()
        sockfile = sock.makefile(mode='rw')
        print('Tester connected')

        while True:
            message = sockfile.readline()
            if message == '':
                break

            process(message, sockfile)


if __name__ == '__main__':
    main()
