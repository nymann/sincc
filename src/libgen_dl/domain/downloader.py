import time
import random
import typer
from pathlib import Path
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup
from libgen_dl.domain.book import Book
from libgen_dl.config import socks_names, user_agents
from aiohttp_socks import ProxyConnector
import pylibgen

class BookDownloader(object):
    async def _download_book(self, book: Book, path: Path, session: ClientSession) -> str:
        async with session.get(url=book.download_url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, features="html.parser")
            anchor_tag = soup.select_one("div#download h2 a[href]")
            url = anchor_tag["href"]
        async with session.get(url=url) as response:
            f = open(path.joinpath(book.filename), "wb")
            while True:
                data = await response.content.read(1024)
                if not data:
                    break
                f.write(data)
            f.close()
        return book.filename

    def prep_request(self):
        random_user_agent = random.choice(user_agents)
        random_sock_name = random.choice(socks_names)
        proxy=ProxyConnector.from_url(f"socks5://{random_sock_name}.mullvad.net:1080")
        headers={
            "User-Agent": random_user_agent,
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "DNT": "1",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "http://libgen.rs/",
            "Cookie": "lg_topic=libgen",
        }
        return proxy, headers
    async def chainer(self, start:float, isbn: str, path: Path):
        proxy, headers = self.prep_request()
        async with ClientSession(headers=headers, connector=proxy) as session:
            pylibgen_lib = pylibgen.Library()
            try:
                self.message(isbn, "Before awaiting")
                book_ids = await self.part1_get_book_ids(isbn=isbn, pylibgen_lib=pylibgen_lib, session=session)
                self.message(isbn, f"Got the book ids", start) 
                libgen_book = await self.part2_get_best_book_from_ids(pylibgen_lib=pylibgen_lib, book_ids=book_ids, session=session)
                self.message(isbn, f"Got the book", start) 
                filename = await self.part3_download_book(libgen_book=libgen_book, isbn=isbn, path=path, session=session)
            except Exception:
                self.message(isbn, "Failed", start=start, err=True)
                return
            self.message(isbn, f"Download complete {filename}", start) 

    def message(self, isbn, msg, start=None, **kwargs):
        parts = [typer.style(f"[{isbn}]", bold=True),typer.style(msg, underline=True)]
        if start:
            parts.append(typer.style(f"({self.elapsed(start)} sec)"))
        typer.echo(" ".join(parts), **kwargs)

    async def part1_get_book_ids(self, pylibgen_lib: pylibgen.Library, isbn: str, session):
        return pylibgen_lib.search(req=isbn, mode="isbn")
    
    async def part2_get_best_book_from_ids(self, pylibgen_lib: pylibgen.Library, book_ids: list[str], session):
        libgen_books = pylibgen_lib.lookup(ids=book_ids, extension="pdf")
        return next(libgen_books)
    
    async def part3_download_book(self, libgen_book, isbn: str, path: Path, session):
        book = Book.from_libgen_book(libgen_book, isbn=isbn)
        return await self._download_book(book=book, path=path, session=session)

    def elapsed(self, start):
        return round((time.perf_counter() - start), 2)
