from abc import ABC, abstractmethod

class BaseHTTP(ABC):
    @abstractmethod
    async def get(self, url):
        pass

    @abstractmethod
    async def head(self, url):
        pass