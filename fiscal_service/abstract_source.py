"""
Provide core fiscal service.
"""
from abc import (
    ABCMeta,
    abstractmethod,
)

from tornado.httpclient import AsyncHTTPClient


class AbstractSource(metaclass=ABCMeta):
    """
    Abstract source.
    """

    @abstractmethod
    async def gather(self, number):
        """
        Gather legal data by fiscal number.
        """

    @staticmethod
    async def fetch_json(url: str):
        client = AsyncHTTPClient(force_instance=True, defaults=dict(
            user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        ))
        try:
            return await client.fetch(url)
        except Exception as e:
            print('Error: %s' % e)
