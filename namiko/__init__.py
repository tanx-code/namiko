import socket
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        # conn.setblocking(False)
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if data == b"":
                    break
                if data:
                    conn.sendall(data)
                    data = None
                else:
                    print("no data")
                    time.sleep(1)