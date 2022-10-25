# coding: utf-8

from typing import Final


class MessageConvert:
    ENCODEING_UTF8: Final = 'utf-8'

    @staticmethod
    def str_to_bytes(data: str) -> bytes:
        return data.encode(MessageConvert.ENCODEING_UTF8)

    def bytes_to_str(data: bytes) -> str:
        return data.decode(MessageConvert.ENCODEING_UTF8)
