import os
import asyncio
from .http import BaseHTTP
from .file import BaseFile
from .reporter import BaseReporter
from .utils import humanbytes

class Download:
    def __init__(self, http_client, file_client, reporter_client, chunck_size=10 * 1024 * 1024):
        self.http_client: BaseHTTP = http_client
        self.file_client: BaseFile = file_client
        self.report_client: BaseReporter = reporter_client
        self.chunk_size = chunck_size
        
    async def _get_content_length(self, url, file_name):
        headers = await self.http_client.head(url)
        content_length = humanbytes(headers.content_length)
        print(f"downloading {file_name} with filesize: {content_length}")
        return content_length


    async def download(self, url):
        file_name = os.path.basename(url)
        content_length = await self._get_content_length(url, file_name)
        response = await self.http_client.get(url)
        task = asyncio.create_task(self.file_client.save(file_name))
        async for chunk in response.content.iter_chunked(self.chunk_size):
            self.report_client.report(chunk, content_length)
            await self.file_client.queue.put(chunk)
        await task