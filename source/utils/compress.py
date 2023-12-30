import json
import zlib


def compress_data(data: dict) -> bytes:
    """
    Serialize to json and compress a data dictionary
    :param data: the data to compress
    :return: the data as a dictionnary
    """

    return zlib.compress(json.dumps(data, ensure_ascii=False).encode("utf-8"))


def uncompress_data(data: bytes) -> dict:
    """
    Decompress and deserialize from json a data dictionary
    :param data: the data to decompress
    :return: the compressed data
    """

    return json.loads(zlib.decompress(data))
