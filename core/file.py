import asyncio
from abc import ABC, abstractmethod

class BaseFile(ABC):
    @abstractmethod
    def __init__(self, queue):
        self.queue: asyncio.Queue = queue

    @abstractmethod
    async def save(self, filename):
        pass
