import os
import asyncio
from .http import BaseHTTP
from .file import BaseFile
from .utils import humanbytes

class Download:
    def __init__(self, http_client, file_client):
        self.http_client: BaseHTTP = http_client
        self.file_client: BaseFile = file_client
        
    async def _get_content_length(self, url):
        headers = await self.http_client.head(url)
        return humanbytes(headers.content_length)

    async def download(self, url):
        name = os.path.basename(url)
        print(f"{name} : {await self._get_content_length(url)}")
        asyncio.create_task(self.file_client.save(name))
        response = await self.http_client.get(url)
        async for chunk in response.content.iter_chunked(10 * 1024 * 1024):
            await self.file_client.queue.put(chunk)