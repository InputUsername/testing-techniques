#!/usr/bin/env python3

import socket
import re
from base import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7890        # Port to listen on (non-privileged ports are > 1023)

import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def to_bool(bl: bool):
    return bl == 'True'

def parse_request(decoded_str: str) -> str:
    match_args = re.findall(r'((?:\w|\d)+)', decoded_str)
    function_name = match_args[0]
    print(match_args)

    match function_name:
        case "CreateUser":
            print("found create-user command")
            (access_token, user_id) = register(match_args[1], match_args[2])
            return access_token

        case "LoginUser":
            print("found login-user command")
            access_token= login(match_args[1], match_args[2])
            return access_token

        case "CreateRoom":
            print("found create-room command")
            print(repr(match_args[1]))
            print(repr(match_args[2]))
            print(repr(match_args[3]))
            room_id = create_room(match_args[1], to_bool(match_args[2]), match_args[3])
            return room_id



    # match decoded_str:
    #     case 


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            received_bytes = conn.recv(1024)
            decoded_str = received_bytes.decode().rstrip()
            print(repr(decoded_str))
            answer_str = parse_request(decoded_str) + "\n"
            print("answer_str: " + answer_str)
            print(repr(answer_str))
            if not received_bytes:
                break
            if answer_str:
                answer_bytes = answer_str.encode()
            print("returning...")
            conn.sendall(answer_bytes)
            print("returned")

#  docker run -d --name synapse --mount type=bind,src=C:\Users\Ruben\testing-techniques\synapse\data,dst=/data -p 8008:8008 matrixdotorg/synapse:latest  
