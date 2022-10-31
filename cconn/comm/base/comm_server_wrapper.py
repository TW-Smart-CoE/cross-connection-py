# coding: utf-8


from typing import Set
from cconn.comm.base.comm_handler import CommHandler
from cconn.utils.topic_utils import TopicUtils


class CommServerWrapper:
    def __init__(self, comm_handler: CommHandler):
        self.comm_handler: CommHandler = comm_handler
        self.__subscribe_topics: Set[str] = set()

    def subscribe(self, topic: str):
        if topic not in self.__subscribe_topics:
            self.__subscribe_topics.add(topic)

    def unsubscribe(self, topic: str):
        self.__subscribe_topics.remove(topic)

    def is_subscribed(self, topic: str):
        for it in self.__subscribe_topics:
            if TopicUtils.is_topic_match(it, topic):
                return True

        return False

    def clear(self):
        self.__subscribe_topics.clear()
