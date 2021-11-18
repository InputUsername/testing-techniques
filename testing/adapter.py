import socket


def process(message: str, sockfile):
    print('received: <' + message.rstrip() + '>')


def main():
    with socket.create_server(('', 7890)) as server:
        sock, addr = server.accept()
        sockfile = sock.makefile('rw')
        print('Tester connected')

        while True:
            message = sockfile.readline()
            if message == '':
                break

            process(message, sockfile)


if __name__ == '__main__':
    main()
