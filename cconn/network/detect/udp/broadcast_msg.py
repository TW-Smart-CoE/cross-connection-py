# coding: utf-8

import struct
from dataclasses import dataclass
from typing import Final

DEFAULT_BROADCAST_FLAG: Final = 0xfffec1e5
BROADCAST_MSG_HEADER_LEN: Final = 12


@dataclass
class BroadcastMsg:
    flag: int = DEFAULT_BROADCAST_FLAG
    ip: int = 0
    port: int = 0
    reserved: int = 0

    def from_bytes(self, buffer: bytes):
        if len(buffer) < BROADCAST_MSG_HEADER_LEN:
            raise Exception(
                'buffer size {0} smaller than BROADCAST_MSG_HEADER_LEN {1}'
                .format(len(buffer), BROADCAST_MSG_HEADER_LEN))

        result = struct.unpack('>IIHH', buffer)
        self.flag = result[0]
        self.ip = result[1]
        self.port = result[2]
        self.reserved = result[3]

    def to_bytes(self, dst_byte_array: bytearray = None) -> bytes:
        if dst_byte_array is None:
            dst_byte_array = bytearray(BROADCAST_MSG_HEADER_LEN)

        struct.pack_into(
            '>IIHH',
            dst_byte_array,
            0,
            self.flag,
            self.ip,
            self.port,
            self.reserved,
        )

        return bytes(dst_byte_array)
