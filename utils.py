import asyncio
import aiohttp


class Downloader:
    def __init__(self):
        self.tasks = []
        self.filenames_links: dict[str, str] = {}

    def add_link(self, filename: str, link: str):
        self.filenames_links[filename] = link

    async def _download_file(self, order_number: int, filename: str, link: str, session: aiohttp.ClientSession):
        async with session.get(link) as response:
            response.raise_for_status()
            content = await response.read()
            with open(filename, "wb") as file:
                file.write(content)
                print("File #{} of {} is downloaded".format(order_number, len(self.filenames_links)))

    async def _prepare(self):
        async with aiohttp.ClientSession() as session:
            for order_number, filename_link in enumerate(self.filenames_links.items(), start=1):
                filename = filename_link[0]
                link = filename_link[1]
                self.tasks.append(self._download_file(order_number, filename, link, session))
            await asyncio.gather(*self.tasks)

    def download(self):
        asyncio.run(self._prepare())



