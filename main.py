import os
import argparse
import asyncio
import aiohttp
from core.download import Download
from core.file import AioFiles
from core.reporter import ConsoleReporter
from core.http import AioHTTP

async def main(urls, path):
    os.chdir(path)
    timeout = aiohttp.ClientTimeout(total=None)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        download = Download(AioHTTP(session), AioFiles(), ConsoleReporter())
        tasks = [asyncio.create_task(download.download(url)) for url in urls]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        for result in result:
            if isinstance(result, Exception):
                print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="*", type=str, required=True)
    parser.add_argument("--path", type=str, default=os.getcwd())
    args = parser.parse_args()
    asyncio.run(main(args.urls, args.path))