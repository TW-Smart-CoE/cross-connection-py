# coding: utf-8

from socket import socket
from src.comm.base.comm import Comm


class TcpComm(Comm):
    def __init__(self, tcp_socket: socket, address: str, port: int):
        self.__tcp_socket: socket = tcp_socket
        self.__address: str = address
        self.__port: int = port

    def recv(self, len: int) -> bytes:
        return self.__tcp_socket.recv(len)

    def send(self, data: bytes) -> int:
        return self.__tcp_socket.send(data)

    def connect(self):
        self.__tcp_socket.connect((self.__address, self.__port))

    def close(self):
        self.__tcp_socket.close()
