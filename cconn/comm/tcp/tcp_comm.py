# coding: utf-8

from socket import socket
from cconn.comm.base.comm import Comm
from cconn.utils.str import bytes_to_hex_format


class TcpComm(Comm):
    def __init__(self, tcp_socket: socket, address: str, port: int):
        self.__tcp_socket: socket = tcp_socket
        self.__address: str = address
        self.__port: int = port

    def recv(self, buf: bytearray, offset: int, length: int) -> int:
        data = self.__tcp_socket.recv(length)
        buf[offset:] = data
        return len(data)

    def send(self, data: bytes) -> int:
        return self.__tcp_socket.send(data)

    def connect(self):
        self.__tcp_socket.connect((self.__address, self.__port))

    def close(self):
        self.__tcp_socket.close()
