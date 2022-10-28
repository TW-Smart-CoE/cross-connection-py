# coding: utf-8


from typing import Tuple
from cconn.connection import Method


class TopicMapper:
    @staticmethod
    def to_full_topic(app_topic: str, method: Method) -> str:
        return '{0}/{1}'.format(app_topic, method.name.lower())

    @staticmethod
    def to_app_topic(full_topic: str) -> Tuple[str, Method]:
        splits = full_topic.split('/')
        return '/'.join(splits[:-1]), Method[splits[-1].upper()]
