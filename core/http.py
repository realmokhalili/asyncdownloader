import aiohttp
from abc import ABC, abstractmethod
from .exceptions import InvalidURL

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
            async for chunk in response.content.iter_chunked(10 * 1024 * 1024):
                yield chunk
            

    async def head(self, url):
        try:
            async with self.client.head(url) as response:
                return response
        except aiohttp.InvalidURL as exc:
            raise InvalidURL(exc.url.name)
            