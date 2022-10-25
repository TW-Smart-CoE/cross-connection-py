# coding: utf-8

import struct
from dataclasses import dataclass
from enum import Enum
from src.utils.message_converter import MessageConvert


MSG_HEADER_LEN = 16


class MsgType(Enum):
    PUBLISH = 0
    SUBSCRIBE = 1
    UNSUBSCRIBE = 2


class Method(Enum):
    # Report value periodically or report for value update.
    REPORT = 0

    # Query value, always followed with a REPLY message. (read-only)
    QUERY = 1

    # Reply value to query.
    REPLY = 2

    # Rend a request, always followed with a response message. (write)
    REQUEST = 3

    # Response to request.
    RESPONSE = 4


def msg_flag() -> int:
    return 0xfffeb0d4


@dataclass
class MsgHeader:
    flag: int = msg_flag()
    type: int = MsgType.PUBLISH.value
    method: int = Method.REPORT.value
    topic_len: int = 0
    data_len: int = 0
    check_sum: int = 0
    reserved: int = 0

    def from_bytes(self, buffer: bytes):
        if len(buffer) < MSG_HEADER_LEN:
            raise Exception('buffer size {0} smaller than MSG_HEADER_LEN {1}'
                            .format(len(buffer), MSG_HEADER_LEN))

        result = struct.unpack('>IBBHHHI', buffer)
        self.flag = result[0]
        self.type = result[1]
        self.method = result[2]
        self.topic_len = result[3]
        self.data_len = result[4]
        self.check_sum = result[5]
        self.reserved = result[6]

    def to_bytes(self) -> bytes:
        data = struct.pack(
            '>IBBHHHI',
            self.flag,
            self.type,
            self.method,
            self.topic_len,
            self.data_len,
            self.check_sum,
            self.reserved,
        )

        return data

    def copy(self):
        msg_header = MsgHeader()
        msg_header.from_bytes(self.to_bytes())
        return msg_header


@dataclass
class Msg:
    header: MsgHeader = None
    topic: bytes = None
    data: bytes = None

    def __init__(
        self,
        header: MsgHeader = MsgHeader(),
        topic: bytes = None,
        data: bytes = None,
    ):
        self.header = header
        self.topic = topic
        self.data = data

    def length(self):
        return MSG_HEADER_LEN + self.header.topic_len + self.header.data_len

    def to_bytes(self):
        header_buffer = self.header.to_bytes()


def create_msg(
    msg_type: MsgType,
    method: Method,
    topic: str,
    data: bytes
) -> Msg:
    topic_bytes = MessageConvert.str_to_bytes(topic)

    header = MsgHeader()
    header.type = msg_type
    header.method = method
    header.topic_len = len(topic_bytes)
    header.data_len = len(data)

    return Msg(header, topic_bytes, data)


def calc_checksum(msg: Msg) -> int:
    checksum = 0

    header_copy = msg.header.copy()
    header_copy.check_sum = 0

    header_bytes = header_copy.to_bytes()
    for byte in header_bytes:
        checksum += byte

    for byte in msg.topic:
        checksum += byte

    for byte in msg.data:
        checksum += byte

    return checksum
