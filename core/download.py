import os
import asyncio
from .http import BaseHTTP
from .file import BaseFile

class Download:
    def __init__(self, http_client, file_client):
        self.http_client: BaseHTTP = http_client
        self.file_client: BaseFile = file_client
        self.queue = asyncio.Queue()
        
    def _humanbytes(self, B):
        """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2) # 1,048,576
        GB = float(KB ** 3) # 1,073,741,824
        TB = float(KB ** 4) # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)

    async def _get_content_length(self, url):
        headers = await self.http_client.head(url)
        return self._humanbytes(headers.content_length)

    async def download(self, url):
        name = os.path.basename(url)
        print(f"{name} : {self._get_content_length(url)}")
        response = await self.http_client.get(url)
        async for chunk in response.content.iter_chunked(10 * 1024 * 1024):
            await self.queue.put(chunk)