import socket
import sys
import re
import time

from base import *

if len(sys.argv) < 2:
    print('Usage: python adapter.py <port number>')
    exit(-1)

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
# PORT = 7891

last_redacted_before_sync_id = None

# Store the user id associated with an access token
user_dict = dict()

# Store the latest SYNC time associated with an access token
synchronization_dict = dict()

# Store the m.room.message and m.room.redaction events that still need
# to be synchronized, associated with an access token. Ignores
# events that were sent with that same access token.
unsynchronized_dict = dict()

# Convert a string to a boolean
def to_bool(bl: bool):
    return bl == 'True'

# Escape the event ID to comply with Torxakis/Matrix communication
def escape_event_id(event_id):
    return event_id.replace('$', '%24')

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
            user_id = response.json()['user_id']
            user_dict[access_token] = user_id

            sockfile.write(f'AccessToken("{access_token}")\n')
        else:
            sockfile.write(f'Error({response.status_code})\n')
        
        sockfile.flush()

    # Login a user and return the access token.
    elif command == 'LoginUser':
        response = login(arguments[0], arguments[1])
        if response.status_code == 200:
            access_token = response.json()['access_token']
            user_id = response.json()['user_id']
            user_dict[access_token] = user_id

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
            event_id = escape_event_id(response.json()['event_id'])
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

    # Synchronise and return latest relevant event or ack if none are available
    elif command == 'Synchronise':
        global last_redacted_before_sync_id

        access_token = arguments[0]
        room_id = arguments[1]

        sync_response = None

        # Give the server some time: we are probably trying to synchronize while
        # the server is still processing some event, resulting in false negatives...
        time.sleep(0.05)

        if access_token in synchronization_dict:
            sync_response = sync(access_token, synchronization_dict[access_token])
        else:
            sync_response = sync(access_token)
            unsynchronized_dict[access_token] = []

        data = sync_response.json()

        try:
            synchronization_dict[access_token] = data['next_batch']            
            sender_id = user_dict[access_token]

            events = data['rooms']['join'][room_id]['timeline']['events']
            for event in events:
                message_type = event['type']
                sender = event['sender']
                if message_type == 'm.room.message' and not sender == sender_id:
                    event_id = escape_event_id(event['event_id'])
                    try:
                        if event['content']['msgtype'] == 'm.text':
                            content = event['content']['body']
                            unsynchronized_dict[access_token].append(f'NewMessage("{event_id}", "{content}")')
                    
                    # This is the case when the message was redacted and we cannot access the contents.
                    except KeyError:
                        event_details = get_event(access_token, room_id, event_id).json()

                        if event_details['type'] != 'm.room.message':
                            print('The requested event is not a message, either Matrix or this adapter is bugged...')
                            return

                        # We didn't synchronize before we got the message in our local store. We can no longer
                        # retrieve the contents of the message.
                        last_redacted_before_sync_id = event_id

                elif message_type == 'm.room.redaction' and not sender == sender_id:
                    redact_id = escape_event_id(event['redacts'])

                    message_was_synched = True
                    id_to_remove = None

                    # This redaction event needs to be filtered out: we did not know of the existence of this message
                    # anyhow.
                    if last_redacted_before_sync_id == redact_id:
                        print(f'Was redacted before sync {redact_id}')
                        message_was_synched = False

                    # If the message is still in our local store, we need to remove it.
                    for idx, val in enumerate(unsynchronized_dict[access_token]):
                        if redact_id in val:
                            message_was_synched = False
                            id_to_remove = idx

                    # We already know of this message, so send out the redaction event.
                    if message_was_synched:
                        unsynchronized_dict[access_token].append(f'MessageRedacted("{redact_id}")')

                    # Remove the send message as it is no longer useful.
                    if id_to_remove:
                        unsynchronized_dict[access_token].pop(id_to_remove)

        except KeyError as e:
            pass

        # No unsychronized events, Acknowledge
        if len(unsynchronized_dict[access_token]) < 1:
            sockfile.write(f'Ack\n')

        # Pop the fist event and return
        else:
            e = unsynchronized_dict[access_token].pop(0)
            sockfile.write(f'{e}\n')

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
