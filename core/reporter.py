from abc import ABC, abstractmethod
from .utils import humanbytes


class BaseReporter(ABC):
    @abstractmethod
    async def report(self, chunck: bytes, file_size: str):
        pass


class ConsoleReporter(ABC):
    def __init__(self):
        self.downloaded = 0

    def report(self, chunck: bytes, file_size: str):
        self.downloaded += len(chunck)
        print(f"{humanbytes(self.downloaded)}/{file_size}", end="\r")