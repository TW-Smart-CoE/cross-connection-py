# coding: utf-8

from unittest import TestCase
from cconn.comm.base.msg import Method
from cconn.comm.base.topic_mapper import TopicMapper


class TestTopicMapper(TestCase):
    def test_to_full_topic(self):
        self.assertEqual('car/command/report', TopicMapper.to_full_topic('car/command', Method.REPORT))
        self.assertEqual('car/command/request', TopicMapper.to_full_topic('car/command', Method.REQUEST))
        self.assertEqual('car/command/response', TopicMapper.to_full_topic('car/command', Method.RESPONSE))
        self.assertEqual('car/command/query', TopicMapper.to_full_topic('car/command', Method.QUERY))
        self.assertEqual('car/command/reply', TopicMapper.to_full_topic('car/command', Method.REPLY))

        self.assertEqual('/request', TopicMapper.to_full_topic('', Method.REQUEST))

        self.assertEqual('/car/command/reply', TopicMapper.to_full_topic('/car/command', Method.REPLY))
        self.assertEqual('$car/command/report', TopicMapper.to_full_topic('$car/command', Method.REPORT))
    
    def test_to_app_topic(self):
        topic, method = TopicMapper.to_app_topic('car/command/report')
        self.assertEqual('car/command', topic)
        self.assertEqual(Method.REPORT, method)

        result = TopicMapper.to_app_topic('car/command/response')
        self.assertEqual('car/command', result[0])
        self.assertEqual(Method.RESPONSE, result[1])

        topic, method = TopicMapper.to_app_topic('/car/command/request')
        self.assertEqual('/car/command', topic)
        self.assertEqual(Method.REQUEST, method)

        topic, method = TopicMapper.to_app_topic('$car/command/query')
        self.assertEqual('$car/command', topic)
        self.assertEqual(Method.QUERY, method)

        topic, method = TopicMapper.to_app_topic('command/reply')
        self.assertEqual('command', topic)
        self.assertEqual(Method.REPLY, method)
