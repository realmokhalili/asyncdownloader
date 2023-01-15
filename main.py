
import argparse
import asyncio
import aiohttp
from core.download import Download
from core.file import AioFiles
from core.reporter import ConsoleReporter

async def main(urls):
    async with aiohttp.ClientSession() as session:
        download = Download(session, AioFiles(), ConsoleReporter())
        tasks = [asyncio.create_task(download.download(url)) for url in urls]
        await asyncio.gather(*tasks)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="*", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(main(args.urls))