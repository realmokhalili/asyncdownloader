import os
from .http import BaseHTTP
from .file import BaseFile
from .reporter import BaseReporter

class Download:
    def __init__(self, http_client, file_client, reporter_client, chunck_size=10 * 1024 * 1024):
        self.http_client: BaseHTTP = http_client
        self.file_client: BaseFile = file_client
        self.report_client: BaseReporter = reporter_client
        self.chunk_size = chunck_size
        
    async def _get_content_length(self, url):
        headers = await self.http_client.head(url)
        return headers.content_length


    async def download(self, url):
        file_name = os.path.basename(url)
        content_length = await self._get_content_length(url)
        response = await self.http_client.get(url)
        file = self.file_client.save(file_name)
        await file.asend(None)
        reporter = self.report_client.report(content_length, file_name)
        reporter.send(None)
        async for chunck in response.content.iter_chunked(self.chunk_size):
            await file.asend(chunck)
            reporter.send(chunck)
