import socket
import sys
import re

from base import *

if len(sys.argv) < 2:
    print('Usage: python adapter.py <port number>')
    exit(-1)

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
# PORT = 7891

# Convert a string to a booelan
def to_bool(bl: bool):
    return bl == 'True'

"""
Process a TorXakis request into a Matrix request.
"""
def process(message, sockfile):
    pattern = '(.+)\((.+)*\)'
    match = re.search(pattern, message)

    if not match:
        print(f'WARN: unknown input {message}')
        return

    command =  match.group(1)
    arguments = match.group(2)
    arguments = re.sub('["]', '', arguments.replace(' ', '')).split(',')

    """
    Matrix requests types supported by this adapter.

    Following the endpoints as described at https://matrix.org/docs/spec/client_server/r0.6.1
    """
    # Register a user and return the access token.
    if command == 'RegisterUser':
        response = register(arguments[0], arguments[1])
        if response.status_code == 200:
            access_token = response.json()['access_token']
            sockfile.write(f'AccessToken("{access_token}")\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        
        sockfile.flush()

    # Login a user and return the access token.
    elif command == 'LoginUser':
        response = login(arguments[0], arguments[1])
        if response.status_code == 200:
            access_token = response.json()['access_token']
            sockfile.write(f'AccessToken("{access_token}")\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        sockfile.flush()

    # Create a room and return the room id.
    elif command == 'CreateRoom':
        response = create_room(arguments[0], to_bool(arguments[1]), arguments[2])
        if response.status_code == 200:
            room_id = response.json()['room_id']
            sockfile.write(f'RoomId("{room_id}")\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        sockfile.flush()

    # Join a room and send Acknowledgement.
    elif command == 'JoinRoom':
        response = join_room(arguments[0], arguments[1])
        if response.status_code == 200:
            sockfile.write('Ack\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        sockfile.flush()

    # Send a message in a room and return the event id.
    elif command == 'SendMessage':
        response = send_message(arguments[0], arguments[1], arguments[2], arguments[3])
        if response.status_code == 200:
            event_id = response.json()['event_id'].replace('$', '%24')
            sockfile.write(f'EventId("{event_id}")\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        sockfile.flush()

    # Redact and send Acknowledgement.
    elif command == 'RedactMessage':
        response = redact(arguments[0], arguments[1], arguments[2], arguments[3])
        if response.status_code == 200:
            sockfile.write('Ack\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        sockfile.flush()

    else:
        print(f'WARN: unknown command \'{command}\'')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Tester connected')
            sockfile = conn.makefile(mode='rw')
            while True:
                message = conn.recv(1024).decode().rstrip()
                if message == '':
                    break
                if message:
                    process(message, sockfile)

if __name__ == '__main__':
    main()
