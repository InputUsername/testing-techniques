import socket
import re

from enum import Enum
from base import *


"""
Matrix requests types supported by this adapter.

Following the endpoints as described at https://matrix.org/docs/spec/client_server/r0.6.1
"""
class MatrixRequests(Enum):
    # No official Matrix command. This uses the interactive authentication API
    # to create an access token for a user.
    AUTHORIZE = 'Authorize'

    # 5.6.1   POST /_matrix/client/r0/register?kind=user
    REGISTER = 'Register'

    # 5.5.2   POST /_matrix/client/r0/login
    LOGIN = 'Login'

    # 10.1.1   POST /_matrix/client/r0/createRoom
    CREATE_ROOM = 'CreateRoom'

"""
Process a TorXakis request into a Matrix request.

[<request_type> <authentication_type> <optional_authentication_token> <request_body_arguments>]
"""
def process(message: str, sockfile):
    # The command, followed by an opening paranthesis, followed by any number of arguments, 
    # follow by a closing paranthesis.
    pattern = '(.+)\((.+)*\)'
    match = re.search(pattern, message)

    if match:
        command = match.group(1)
        arguments = match.group(2)
        arguments = re.sub('["]', '', arguments)

        argument_list = arguments.split(',')

        print(f'cmd: {command}, args: {argument_list}')

        try:
            request = MatrixRequests(command)

            match request:
                case MatrixRequests.AUTHORIZE:
                    # token = acquire_session_token()
                    sockfile.write(f'Bearer("token")')
                case MatrixRequests.REGISTER:
                    print("REGISTER")
                    sockfile.write("200\n")
                    sockfile.flush()
                case MatrixRequests.LOGIN:
                    print("LOGIN")
                case MatrixRequests.CREATE_ROOM:
                    print("CREATE ROOM")

        except ValueError as e:
            print(f"Unknown command '{command}'")

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
