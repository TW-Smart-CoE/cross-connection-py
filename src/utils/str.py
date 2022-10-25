# coding: utf-8


def bytes_to_hex_format(data) -> str:
    return ''.join('%02x ' % b for b in data)
