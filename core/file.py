import aiofiles
from abc import ABC, abstractmethod, abstractproperty
from asyncio import Queue


class BaseFile(ABC):
    @abstractmethod
    async def save(self, file_name):
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
    
    async def save(self, file_name):
        async with aiofiles.open(file_name, mode="wb") as file:
            while not self.queue.empty():
                chunck = await self.queue.get()
                await file.write(chunck)
        print(f"successfully downloaded {file_name}")