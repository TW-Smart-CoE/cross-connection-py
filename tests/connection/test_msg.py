# coding: utf-8

from unittest import TestCase
from src.comm.base.msg import Method
from src.comm.base.msg import MsgHeader
from src.comm.base.msg import MsgType


class TestMsg(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test(self):
        msg_header = MsgHeader()
        msg_header.type = MsgType.UNSUBSCRIBE.value
        msg_header.method = Method.QUERY.value
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
