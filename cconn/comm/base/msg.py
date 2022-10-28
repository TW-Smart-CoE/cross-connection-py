# coding: utf-8

from email import header
import struct
from dataclasses import dataclass
from enum import Enum
from cconn.utils.message_converter import MessageConverter


MSG_HEADER_LEN = 16
MSG_FLAG = 0xfffeb0d4


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


@dataclass
class MsgHeader:
    flag: int = MSG_FLAG
    type: MsgType = MsgType.PUBLISH
    method: Method = Method.REPORT
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
        self.type = MsgType(result[1])
        self.method = Method(result[2])
        self.topic_len = result[3]
        self.data_len = result[4]
        self.check_sum = result[5]
        self.reserved = result[6]

    def to_bytes(self, dst_byte_array: bytearray = None) -> bytes:
        if dst_byte_array is None:
            dst_byte_array = bytearray(MSG_HEADER_LEN)

        struct.pack_into(
            '>IBBHHHI',
            dst_byte_array,
            0,
            self.flag,
            self.type.value,
            self.method.value,
            self.topic_len,
            self.data_len,
            self.check_sum,
            self.reserved,
        )

        return bytes(dst_byte_array)

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
        header: MsgHeader = None,
        topic: bytes = None,
        data: bytes = None,
    ):
        self.header = header or MsgHeader()
        self.topic = topic
        self.data = data

    def __topic_len(self) -> int:
        return 0 if self.topic is None else len(self.topic)

    def __data_len(self) -> int:
        return 0 if self.data is None else len(self.data)

    def length(self) -> int:
        return MSG_HEADER_LEN + self.__topic_len() + self.__data_len()

    def prepare(self):
        if self.topic is None:
            raise Exception('topic is None')

        self.header.topic_len = len(self.topic)
        self.header.data_len = 0 if self.data is None else len(self.data)
        self.header.check_sum = calc_checksum(self)

    def to_bytes(self) -> bytes:
        byte_arr = bytearray(self.length())
        self.header.to_bytes(byte_arr)

        byte_arr[MSG_HEADER_LEN:MSG_HEADER_LEN + len(self.topic)] = self.topic
        if self.data is not None:
            byte_arr[MSG_HEADER_LEN + len(self.topic):
                     MSG_HEADER_LEN + len(self.topic)
                     + len(self.data)] = self.data

        return bytes(byte_arr)

    def copy(self):
        return Msg(
            header=self.header.copy(),
            topic=self.topic,
            data=self.data
        )


def create_msg(
    msg_type: MsgType,
    method: Method,
    topic: str,
    data: bytes
) -> Msg:
    topic_bytes = MessageConverter.str_to_bytes(topic)

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

    if msg.data is not None:
        for byte in msg.data:
            checksum += byte

    return checksum
