import aiofiles
from abc import ABC, abstractmethod, abstractproperty
from asyncio import Queue


class BaseFile(ABC):
    @abstractmethod
    async def save(self, filename):
        pass

    @abstractproperty
    def queue(self):
        pass


class AioFiles(BaseFile):
    def __init__(self):
        self._queue = Queue()

    @property
    def queue(self):
        return self._queue
    
    async def save(self, filename):
        async with aiofiles.open(filename, mode="wb") as file:
            while True:
                chunck = await self.queue.get()
                await file.write(chunck)