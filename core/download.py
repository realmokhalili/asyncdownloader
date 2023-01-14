import os
import asyncio
from .http import BaseHTTP
from .file import BaseFile
from .reporter import BaseReporter
from .utils import humanbytes

class Download:
    def __init__(self, http_client, file_client, reporter_client):
        self.http_client: BaseHTTP = http_client
        self.file_client: BaseFile = file_client
        self.report_client: BaseReporter = reporter_client
        
    async def _get_content_length(self, url, file_name):
        headers = await self.http_client.head(url)
        content_length = humanbytes(headers.content_length)
        print(f"downloading {file_name} with filesize: {content_length}")
        return content_length


    async def download(self, url):
        file_name = os.path.basename(url)
        content_length = await self._get_content_length(url, file_name)
        asyncio.create_task(self.file_client.save(file_name))
        response = await self.http_client.get(url)
        async for chunk in response.content.iter_chunked(10 * 1024 * 1024):
            self.report_client.report(chunk, content_length)
            await self.file_client.queue.put(chunk)
        print(f"successfully downloaded {file_name}")