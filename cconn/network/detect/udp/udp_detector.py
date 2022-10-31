# coding: utf-8

import ipaddress
from socket import (
    socket,
    AF_INET,
    SOCK_DGRAM,
    SOL_SOCKET,
    SO_BROADCAST
)
from typing import Callable, Dict, Final
from cconn.log.logger import DefaultLogger, Logger
from cconn.network.detect.network_detector import NetworkDetector
from cconn.definitions.prop_keys import PropKeys
from cconn.utils.props import PropsUtils
from cconn.network.detect.udp.broadcast_msg import (
    BROADCAST_MSG_HEADER_LEN,
    DEFAULT_BROADCAST_FLAG,
    BroadcastMsg,
)


class UdpDetector(NetworkDetector):
    ANY_ADDRESS: Final = "0.0.0.0"
    DEFAULT_BROADCAST_PORT: Final = 12000
    DEFAULT_BROADCAST_INTERVAL: Final = 10
    RECV_BUF_LEN: Final = 32

    def __init__(self):
        self.__logger = DefaultLogger()
        self.__receiver_sock = None
        self.__broadcast_port = 0
        self.__is_keep_receiving = False
        self.__flag = 0

    def set_logger(self, logger: Logger):
        self.__logger = logger

    def start_discover(
        self,
        config_props: Dict[str, str],
        on_found_service: Callable[[Dict[str, str]], None],
    ):
        self.__broadcast_port = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_UDP_DETECTOR_BROADCAST_PORT,
            UdpDetector.DEFAULT_BROADCAST_PORT,
        )

        self.__flag = PropsUtils.get_prop_int(
            config_props,
            PropKeys.PROP_UDP_DETECTOR_FLAG,
            DEFAULT_BROADCAST_FLAG,
        )

        self.__receiver_sock = socket(AF_INET, SOCK_DGRAM)
        self.__receiver_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.__receiver_sock.bind(('', self.__broadcast_port))
        self.__is_keep_receiving = True

        while self.__is_keep_receiving and self.__receiver_sock is not None:
            self.__logger.debug(
                'Waiting for broadcast on port {0}'
                .format(self.__broadcast_port))

            data = self.__receiver_sock.recvfrom(UdpDetector.RECV_BUF_LEN)
            if len(data[0]) == BROADCAST_MSG_HEADER_LEN:
                broadcastMsg = BroadcastMsg()
                broadcastMsg.from_bytes(data[0])
                if broadcastMsg.flag == self.__flag:
                    props = dict()
                    props[PropKeys.PROP_UDP_DETECTOR_ON_FOUND_SERVICE_IP] \
                        = str(ipaddress.IPv4Address(broadcastMsg.ip))
                    props[PropKeys.PROP_UDP_DETECTOR_BROADCAST_PORT] \
                        = broadcastMsg.port

                    on_found_service(props)

    def stop_discover(self):
        self.__is_keep_receiving = False

        try:
            if self.__receiver_sock is not None:
                self.__receiver_sock.close()
                self.__receiver_sock = None
        except Exception as e:
            self.__logger.error(str(e))
