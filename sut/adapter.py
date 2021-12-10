#!/usr/bin/env python3

import socket
import re
from base import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7890        # Port to listen on (non-privileged ports are > 1023)

def to_bool(bl: bool):
    return bl == 'True'

def parse_request(decoded_str: str) -> str:
    match_args = re.findall(r'((?:[^(",)])+)', decoded_str)
    function_name = match_args[0]

    match function_name:
        case "CreateUser":
            (access_token, _) = register(match_args[1], match_args[2])
            return access_token

        case "LoginUser":
            access_token= login(match_args[1], match_args[2])
            return access_token

        case "CreateRoom":
            room_id = create_room(match_args[1], to_bool(match_args[2]), match_args[3])
            return str(room_id)

        case "JoinRoom":
            room_id = join_room(match_args[1], match_args[2])
            str_room_id = str(room_id)
            return str_room_id
        case _:
            return ""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            received_bytes = conn.recv(1024)
            decoded_str = received_bytes.decode().rstrip()
            print("Received: " + repr(decoded_str))
            answer_str = parse_request(decoded_str) + "\n"
            print("Returning: " + answer_str)
            if not received_bytes:
                break    
            answer_bytes = answer_str.encode()
            conn.sendall(answer_bytes)
            
#  docker run -d --name synapse --mount type=bind,src=C:\Users\Ruben\testing-techniques\synapse\data,dst=/data -p 8008:8008 matrixdotorg/synapse:latest  
