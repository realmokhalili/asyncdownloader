import asyncio
import aiohttp
from core.download import Download
from core.file import AioFiles

async def main():
    async with aiohttp.ClientSession() as session:
        download = Download(session, AioFiles())
        await download.download("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1200px-Image_created_with_a_mobile_phone.png")



if __name__ == "__main__":
    asyncio.run(main())