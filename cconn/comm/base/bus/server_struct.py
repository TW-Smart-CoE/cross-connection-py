# coding: utf-8

from dataclasses import dataclass
from cconn.network.register.network_register import NetworkRegister
from cconn.server import Server


@dataclass
class ServerStruct:
    server: Server
    register: NetworkRegister
