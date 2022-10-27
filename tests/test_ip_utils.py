# coding: utf-8

import ipaddress
from unittest import TestCase


class TestIpUtils(TestCase):
    def test_ip_convert(self):
        ip_str = '192.168.1.1'
        ip = int(ipaddress.IPv4Address(ip_str))
        output = str(ipaddress.IPv4Address(ip))

        self.assertEqual(ip_str, output)