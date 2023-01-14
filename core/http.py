import aiohttp
from abc import ABC, abstractmethod

class BaseHTTP(ABC):
    @abstractmethod
    async def get(self, url):
        pass

    @abstractmethod
    async def head(self, url):
        pass


class AioHTTP(BaseHTTP):
    def __init__(self, client):
        self.client: aiohttp.ClientSession = client

    async def get(self, url):
        async with self.client.get(url) as response:
            return response

    async def head(self, url):
        async with self.client.head(url) as response:
            return response