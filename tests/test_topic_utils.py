# coding: utf-8

from unittest import TestCase
from cconn.comm.base.msg import Method
from cconn.comm.base.topic_mapper import TopicMapper
from cconn.utils.topic_utils import TopicUtils


class TestTopicUtils(TestCase):
    def test_topic_match_exact(self):
        self.assertTrue(TopicUtils.is_topic_match("/sys/device/get", "/sys/device/get"))
        self.assertFalse(TopicUtils.is_topic_match("/sys/device/get", "/sys/device/set"))
        self.assertFalse(TopicUtils.is_topic_match("/sys/device/get", "/sys/device"))

    def test_topic_match_with_plus(self):
        self.assertTrue(TopicUtils.is_topic_match("/sys/+/get", "/sys/xx/get"))
        self.assertFalse(TopicUtils.is_topic_match("/sys/+/get", "/sys/xx/set"))
        self.assertTrue(TopicUtils.is_topic_match("/sys/+/+", "/sys/xx/set"))
        self.assertTrue(TopicUtils.is_topic_match("/sys/+/+/test", "/sys/xx/set/test"))
        self.assertFalse(TopicUtils.is_topic_match("/sys/+/+/test", "/sys/xx/set/mock"))

    def test_topic_match_with_sharp(self):
        self.assertTrue(TopicUtils.is_topic_match("/sys/#", "/sys/xx/get"))
        self.assertFalse(TopicUtils.is_topic_match("/sys/#", "/ays/xx/get"))
        self.assertTrue(TopicUtils.is_topic_match(TopicMapper.to_full_topic("/sys/#", Method.REQUEST), TopicMapper.to_full_topic("/sys/abc/xyz", Method.REQUEST)))
        self.assertFalse(TopicUtils.is_topic_match(TopicMapper.to_full_topic("/sys/#", Method.REQUEST), TopicMapper.to_full_topic("/sys/abc/xyz", Method.RESPONSE)))
    