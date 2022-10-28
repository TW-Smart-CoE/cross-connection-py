# coding: utf-8


class TopicUtils:
    @staticmethod
    def is_topic_match(topic_filter: str, topic: str) -> bool:
        topic_filter_tokens = topic_filter.split('/')
        topic_tokens = topic.split('/')

        if len(topic_filter_tokens) > len(topic_tokens):
            return False

        for idx, _ in enumerate(topic_filter_tokens):
            topic_filter_token = topic_filter_tokens[idx]
            topic_token = topic_tokens[idx]

            if '#' == topic_filter_token:
                filter_last_token = \
                    topic_filter_tokens[len(topic_filter_tokens) - 1]
                last_token = topic_tokens[len(topic_tokens) - 1]

                return True if filter_last_token == '#' \
                    else filter_last_token == last_token

            if '+' != topic_filter_token and topic_filter_token != topic_token:
                return False

        return len(topic_filter_tokens) == len(topic_tokens)
