from pathlib import Path
from asyncio import run
from time import perf_counter

from requests import get
from aiohttp import ClientSession
from aiofiles import open as async_open


DIR = Path(__file__).parent


def download_files_synchronously():
    '''
    Creates `out_sync` directory, clears it and reads `links.txt`.
    Separately gets content from every link and saves it to files respectively.
    '''
    out_dir = DIR.joinpath('out_sync')
    out_dir.mkdir(parents=True, exist_ok=True)
    [f.unlink() for f in out_dir.iterdir()]

    with open(f'{DIR}\links.txt') as links_file:
        links = links_file.readlines()

    for link in links:
        link = link.replace('\n', '')
        filename = link.split('/')[-1]
        response = get(link)

        with open(f'{out_dir}\{filename}', 'wb') as out_file:
            out_file.write(response.content)


async def download_files_asynchronously():
    '''
    Creates `out_async` directory, clears it and asynchronously reads `links.txt`.
    Asynchronously gets content from every link and saves it to files respectively.
    '''
    out_dir = DIR.joinpath('out_async')
    out_dir.mkdir(parents=True, exist_ok=True)
    [f.unlink() for f in out_dir.iterdir()]

    async with async_open(f'{DIR}\links.txt') as links_file:
        async for link in links_file:
            link = link.replace('\n', '')
            filename = link.split('/')[-1]

            async with ClientSession() as session:
                async with session.get(link) as resp:
                    content = await resp.read()

            async with async_open(f'{out_dir}\{filename}', 'wb') as out_file:
                await out_file.write(content)


if __name__ == '__main__':
    # Comparing execution time of both algorithms.
    sync_time = perf_counter()
    download_files_synchronously()
    print(f'Synchronous execution time: {perf_counter() - sync_time:0.2f} msecs.')

    async_time = perf_counter()
    run(download_files_asynchronously())
    print(f'Asynchronous execution time: {perf_counter() - async_time:0.2f} msecs.')
