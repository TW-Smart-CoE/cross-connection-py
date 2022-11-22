# coding: utf-8

import ipaddress
import socket


class AddressUtils:
    @staticmethod
    def hostname() -> str:
        return socket.gethostname()

    @staticmethod
    def host_address() -> str:
        """Try to determine the local IP address of the machine."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Use Google Public DNS server to determine own IP
            sock.connect(('8.8.8.8', 80))
            return sock.getsockname()[0]
        except socket.error:
            try:
                hostname = AddressUtils.hostname()
                if hostname == 'raspberrypi':
                    hostname = f'{hostname}.local'
                return socket.gethostbyname(hostname)
            except socket.gaierror:
                return '127.0.0.1'
        finally:
            sock.close()

    @staticmethod
    def ipv4_str_to_int(ipv4: str) -> int:
        return int(ipaddress.IPv4Address(ipv4))

    @staticmethod
    def ipv4_int_to_str(ipv4: int) -> str:
        return str(ipaddress.IPv4Address(ipv4))
