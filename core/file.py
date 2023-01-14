import aiofiles
from abc import ABC, abstractmethod



class BaseFile(ABC):
    @abstractmethod
    async def save(self, file_name):
        pass

class AioFiles(BaseFile):

    async def save(self, file_name):
        async with aiofiles.open(file_name, mode="wb") as file:
            while True:
                chunck = yield
                await file.write(chunck)