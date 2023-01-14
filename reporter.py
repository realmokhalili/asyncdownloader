import asyncio
from abc import ABC, abstractmethod


class BaseReporter(ABC):
    abstractmethod
    def __init__(self, queue):
        self.queue: asyncio.Queue = queue

    @abstractmethod
    async def report(self):
        pass