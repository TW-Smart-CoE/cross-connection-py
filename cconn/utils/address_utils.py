# coding: utf-8

import ipaddress
import socket


class AddressUtils:
    @staticmethod
    def hostname() -> str:
        return socket.gethostname()

    @staticmethod
    def host_address() -> str:
        try:
            hostname = AddressUtils.hostname()
            if hostname == 'raspberrypi':
                hostname = f'{hostname}.local'

            return socket.gethostbyname(hostname)
        except Exception as e:
            print(e)
            return ''

    @staticmethod
    def ipv4_str_to_int(ipv4: str) -> int:
        return int(ipaddress.IPv4Address(ipv4))

    @staticmethod
    def ipv4_int_to_str(ipv4: int) -> str:
        return str(ipaddress.IPv4Address(ipv4))
