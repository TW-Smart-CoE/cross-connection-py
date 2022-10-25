# coding: utf-8

from typing import Final


class PropKeys:
    PROP_IP: Final = 'ip'
    PROP_PORT: Final = 'port'
    PROP_AUTO_CONNECT: Final = 'auto_reconnect'
    PROP_MIN_RECONNECT_RETRY_TIME: Final = "min_reconnect_retry_time"
    PROP_MAX_RECONNECT_RETRY_TIME: Final = "max_reconnect_retry_time"

    PROP_UDP_DETECTOR_BROADCAST_PORT: Final = 'broadcast_port'
    PROP_UDP_DETECTOR_FLAG = 'flag'
    PROP_UDP_DETECTOR_ON_FOUND_SERVICE_IP: Final = 'server_ip'
    PROP_UDP_DETECTOR_ON_FOUND_SERVICE_PORT: Final = 'server_port'

    PROP_UDP_REGISTER_BROADCAST_PORT: Final = 'broadcast_port'
    PROP_UDP_REGISTER_BROADCAST_INTERVAL: Final = 'broadcast_interval'
    PROP_UDP_REGISTER_FLAG: Final = 'flag'
    PROP_UDP_REGISTER_SERVER_IP: Final = 'server_ip'
    PROP_UDP_REGISTER_SERVER_PORT: Final = 'server_port'
