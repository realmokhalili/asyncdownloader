import argparse
import asyncio
import aiohttp
from core.download import Download
from core.file import AioFiles
from core.reporter import ConsoleReporter
from core.http import AioHTTP

async def main(urls):
    async with aiohttp.ClientSession() as session:
        download = Download(AioHTTP(session), AioFiles(), ConsoleReporter())
        tasks = [asyncio.create_task(download.download(url)) for url in urls]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        for result in result:
            if isinstance(result, Exception):
                print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="*", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(main(args.urls))