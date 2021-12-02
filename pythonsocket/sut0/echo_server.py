#!/usr/bin/env python3

import socket
import re

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7890        # Port to listen on (non-privileged ports are > 1023)

import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parse_request(decoded_str: str) -> str:
    match_func = re.match(r'(\w+)\(.*\)', decoded_str)
    function_name = match_func.group(1)
    print(function_name)
    match_args = re.findall(r'(?<=")(\w*|\d*)(?=")  ', decoded_str)
    print(match_args)
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
            answer_str = parse_request(decoded_str)
            if not received_bytes:
                break
            if answer_str:
                answer_bytes = answer_str.encode()
            # conn.sendall(answer_bytes)
            print("return test")
            conn.sendall("test\n".encode())
            print("test returned")



# /*
# TorXakis - Model Based Testing
# Copyright (c) 2015-2021 TNO and Radboud University
# See LICENSE at root directory of this repository.
# */

# import java.net.*;
# import java.io.*;

# public class QueueServer0 {
#     public static void main(String[] args) {
#         if (args.length < 1) {
#             System.out.println("own port number required");
#             return;
#         }
#         try {
#             int portNo = Integer.parseInt(args[0]);

#             ServerSocket serverSocket = new ServerSocket(portNo);
#             System.out.println("Waiting for tester");
#             Socket sock = serverSocket.accept();

#             InputStream inStream = sock.getInputStream();
#             BufferedReader socketReader = new BufferedReader(new InputStreamReader(inStream));

#             OutputStream outStream = sock.getOutputStream();
#             PrintWriter socketWriter = new PrintWriter(new OutputStreamWriter(outStream));
#             System.out.println("Tester connected.");

#             Queue q = new Queue();
#             while (true) {
#                 q.show();
#                 String s = socketReader.readLine().trim();
#                 processInput(s, q, socketWriter);
#                 socketWriter.flush();
#             }
#         } catch (Exception ex) {
#             ex.printStackTrace();
#         }
#     }

#     private static void processInput(String s, Queue q, PrintWriter socketWriter) {
#         if (s.startsWith("Enq")) {
#             int sep1 = s.indexOf("(");
#             int sep2 = s.indexOf(")");
#             int x = Integer.parseInt(s.substring(sep1 + 1, sep2).trim());
#             q.add(x);
#         } else if (s.startsWith("Deq")) {
#             if (!q.empty()) {
#                 socketWriter.print(q.take() + "\n");
#             }
#         }
#     }
# }

# class Queue {
#     private Cell first = null;
#     private Cell last = null;

#     public void add(int x) {
#         Cell cell = new Cell();
#         cell.data = x;
#         cell.rest = null;
#         if (empty()) {
#             first = cell;
#         } else {
#             last.rest = cell;
#         }
#         last = cell;
#     }

#     public boolean empty() {
#         return (first == null);
#     }

#     public int take() {
#         Cell cell = first;
#         first = cell.rest;
#         return (cell.data);
#     }

#     public void show() {
#         System.out.print("[ ");
#         Cell cell = first;
#         while (cell != null) {
#             System.out.print(cell.data);
#             cell = cell.rest;
#             if (cell != null) {
#                 System.out.print(", ");
#             }
#         }
#         System.out.println(" ]");
#     }
# }

# class Cell {
#     public int data;
#     public Cell rest;
# }
