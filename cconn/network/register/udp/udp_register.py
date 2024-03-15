# coding: utf-8

import time
from socket import (
    socket,
    AF_INET,
    SOCK_DGRAM,
    SOL_SOCKET,
    SO_BROADCAST
)
from threading import Thread
from typing import Dict, Final
from cconn.definitions.prop_keys import PropKeys
from cconn.log.logger import DefaultLogger, Logger
from cconn.network.detect.udp.broadcast_header import (
    DEFAULT_BROADCAST_FLAG,
    BroadcastHeader
)
from cconn.network.register.network_register import NetworkRegister
from cconn.utils.props import PropsUtils
from cconn.utils.address_utils import AddressUtils
from cconn.utils.str import bytes_to_hex_format


class UdpRegister(NetworkRegister):
    ANY_ADDRESS: Final = '0.0.0.0'
    DEFAULT_BROADCAST_PORT: Final = 12000
    DEFAULT_BROADCAST_INTERVAL: Final = 10

    def __init__(self):
        self.__logger: Logger = DefaultLogger()
        self.__is_send_broadcast: bool = False
        self.__broadcast_interval: int = 0
        self.__server_ip: str = ''
        self.__server_port: int = 0
        self.__broadcast_port: int = 0
        self.__flag: int = 0
        self.__data: bytes = None
        self.__socket: socket = None
        self.__debug_mode = False

    def set_logger(self, logger: Logger):
        self.__logger = logger

    def __send_broadcast_task(self):
        while self.__is_send_broadcast:
            try:
                data = self.__build_broadcast_header()
                if self.__data is not None:
                    data += self.__data
                
                if self.__debug_mode:
                    self.__logger.debug(f'send data (len={len(data)}): {bytes_to_hex_format(data)}')
                
                self.__socket.sendto(data,
                                     ('<broadcast>', self.__broadcast_port))
            except Exception as e:
                self.__logger.error(f'send udp broadcast error: {str(e)}')

            time.sleep(self.__broadcast_interval / 1000)

    def __build_broadcast_header(self) -> bytes:
        broadcast_header = BroadcastHeader()
        broadcast_header.flag = self.__flag
        broadcast_header.ip = AddressUtils.ipv4_str_to_int(self.__server_ip)
        broadcast_header.port = self.__server_port

        return broadcast_header.to_bytes()

    def __start_udp_broadcast(self):
        self.__socket = socket(AF_INET, SOCK_DGRAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.__is_send_broadcast = True

        thread = Thread(target=self.__send_broadcast_task)
        thread.start()

    def register(
        self,
        config_props: Dict[str, object]
    ):
        self.__broadcast_port = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_BROADCAST_PORT,
            UdpRegister.DEFAULT_BROADCAST_PORT,
        )

        self.__broadcast_interval = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_BROADCAST_INTERVAL,
            UdpRegister.DEFAULT_BROADCAST_INTERVAL,
        )

        self.__flag = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_FLAG,
            DEFAULT_BROADCAST_FLAG,
        )

        host_address = AddressUtils.host_address()
        self.__server_ip = PropsUtils.get_prop_str(
            config_props,
            PropKeys.PROP_SERVER_IP,
            host_address
        )

        self.__server_port = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_SERVER_PORT,
            0
        )

        self.__data = PropsUtils.get_prop_bytes(
            config_props,
            PropKeys.PROP_BROADCAST_DATA,
            None
        )

        self.__debug_mode = PropsUtils.get_prop_bool(
            config_props,
            PropKeys.PROP_BROADCAST_DEBUG_MODE,
            False
        )

        self.__start_udp_broadcast()

    def unregister(self):
        self.__is_send_broadcast = False
