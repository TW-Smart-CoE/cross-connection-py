# coding: utf-8

from unittest import TestCase
from cconn.comm.base.msg import Method, MsgType, MsgHeader, Msg, calc_checksum
from cconn.comm.base.msg import MsgHeader
from cconn.comm.base.msg import MsgType
from cconn.utils.message_converter import MessageConverter


class TestMsg(TestCase):
    def test_msg_header(self):
        msg_header = MsgHeader()
        msg_header.type = MsgType.UNSUBSCRIBE
        msg_header.method = Method.QUERY
        msg_header.topic_len = 65534
        msg_header.data_len = 40
        msg_header.check_sum = 3

        bytes = msg_header.to_bytes()

        header = MsgHeader()
        header.from_bytes(bytes)

        self.assertEqual(msg_header.type, header.type)
        self.assertEqual(msg_header.method, header.method)
        self.assertEqual(msg_header.topic_len, header.topic_len)
        self.assertEqual(msg_header.data_len, header.data_len)
        self.assertEqual(msg_header.check_sum, header.check_sum)

    def test_msg(self):
        msg = Msg()
        msg.header.type = MsgType.UNSUBSCRIBE
        msg.header.method = Method.QUERY
        msg.header.check_sum = 0
        msg.topic = MessageConverter.str_to_bytes('/aaaa')
        msg.data = MessageConverter.str_to_bytes('00000000')

        msg.prepare()

        self.assertEqual(len(msg.topic), msg.header.topic_len)
        self.assertEqual(len(msg.data), msg.header.data_len)
        self.assertEqual(msg.header.check_sum, calc_checksum(msg))

    def test_msg2(self):
        msg1 = Msg()
        msg1.header.type = MsgType.SUBSCRIBE
        msg1.header.method = Method.QUERY
        msg1.header.check_sum = 0
        msg1.topic = bytearray(128)
        msg1.data = bytearray(256) 
        msg1.prepare()

        msg2 = Msg()
        msg2.header.type = MsgType.PUBLISH
        msg2.header.method = Method.REQUEST
        msg2.header.check_sum = 0
        msg2.topic = bytearray(188)
        msg2.data = bytearray(512) 
        msg2.prepare()

        msg3 = Msg()
        msg3.header.type = MsgType.UNSUBSCRIBE
        msg3.header.method = Method.RESPONSE
        msg3.header.check_sum = 0
        msg3.topic = bytearray(188)
        msg3.data = bytearray(512) 
        msg3.prepare()
    
    def test_prepare(self):
        msg = Msg(
            header=MsgHeader(
                type=MsgType.SUBSCRIBE,
                method=Method.REQUEST,
            ),
            topic=MessageConverter.str_to_bytes('test'),
        )
        msg.prepare()
