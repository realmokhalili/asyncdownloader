import os
from abc import ABC, abstractmethod
from tqdm import tqdm


class BaseReporter(ABC):
    @abstractmethod
    async def report(self, file_size: str, file_name:str):
        yield


class ConsoleReporter(ABC):
    def report(self, file_size: str, file_name: str):
        with tqdm.wrapattr(
            open(os.devnull, "wb"), "write", miniters=1, desc=file_name, total=file_size
        ) as fout:
            while True:
                chunk = yield
                fout.write(chunk)
