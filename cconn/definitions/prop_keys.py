# coding: utf-8

from typing import Final


class PropKeys:
    PROP_IP: Final = 'ip'
    PROP_PORT: Final = 'port'
    PROP_AUTO_RECONNECT: Final = 'auto_reconnect'
    PROP_MIN_RECONNECT_RETRY_TIME: Final = 'min_reconnect_retry_time'
    PROP_MAX_RECONNECT_RETRY_TIME: Final = 'max_reconnect_retry_time'
    PROP_BROADCAST_PORT: Final = 'broadcast_port'
    PROP_BROADCAST_INTERVAL: Final = 'broadcast_interval'
    PROP_BROADCAST_DATA: Final = 'broadcast_data'
    PROP_BROADCAST_DEBUG_MODE: Final = 'broadcast_debug_mode'
    PROP_FLAG = 'flag'
    PROP_SERVER_IP: Final = 'server_ip'
    PROP_SERVER_PORT: Final = 'server_port'
    PROP_RECV_BUFFER_SIZE: Final = 'recv_buffer_size'
