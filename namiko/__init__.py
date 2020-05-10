"""
FYI:
epoll python api https://docs.python.org/3/library/select.html#edge-and-level-trigger-polling-epoll-objects
"""
import socket
import select

from namiko.http import do_request

from loguru import logger


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def server():
    # 自己保存所有连接
    fd_conn_map = {}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        with select.epoll() as ep:
            # register server fd
            ep.register(s, select.EPOLLIN | select.EPOLLET)

            while 1:
                logger.debug(fd_conn_map)
                events = ep.poll()

                for fd, mask in events:
                    # client connections incoming
                    if s.fileno() == fd:
                        conn, addr = s.accept()
                        logger.debug(f"connection from {conn} {addr}")
                        ep.register(conn, select.EPOLLIN | select.EPOLLET)
                        fd_conn_map[conn.fileno()] = conn
                    # read other sockets
                    else:
                        with fd_conn_map[fd] as conn:
                            do_request(conn)
                        # clean fd
                        ep.unregister(fd)
                        fd_conn_map.pop(fd)
