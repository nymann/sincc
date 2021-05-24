from datetime import datetime as dt
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
    def __init__(self, isbn: str, output_dir: Path, session: ClientSession = None):
        self.isbn = isbn
        self.output_dir = output_dir
        if session is None:
            proxy, headers = self.prep_request()
            self.session = ClientSession(headers=headers, connector=proxy)
        else:
            self.session = session

    async def _download_book(self, book: Book) -> str:
        async with self.session.get(url=book.download_url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, features="html.parser")
            anchor_tag = soup.select_one("div#download h2 a[href]")
            url = anchor_tag["href"]
        async with self.session.get(url=url) as response:
            f = open(self.output_dir.joinpath(book.filename), "wb")
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
    async def chainer(self):
        pylibgen_lib = pylibgen.Library()
        try:
            self.message("STARTED: Getting book ids")
            book_ids = await self.part1_get_book_ids(pylibgen_lib=pylibgen_lib)
            if not book_ids:
                self.message("WARNING: Couldn't find this book.", fg=typer.colors.YELLOW)
                await self.session.close()
                return
            self.message("DONE: Found all version identifiers", fg=typer.colors.GREEN) 
            self.message("STARTED: Finding best suitable version")
            libgen_book = await self.part2_get_best_book_from_ids(pylibgen_lib=pylibgen_lib, book_ids=book_ids)
            if libgen_book is None:
                self.message("WARNING: Something went wrong while fetching the book.", fg=typer.colors.YELLOW)
                await self.session.close()
                return
            self.message("DONE: Found best version.", fg=typer.colors.GREEN) 
            await self.part3_download_book(libgen_book=libgen_book)
        except Exception as e:
            self.message(f"FAILED: {e}", fg=typer.colors.RED, err=True)
            await self.session.close()
            return
        self.message(f"DONE: Downloaded pdf", fg=typer.colors.GREEN) 
        await self.session.close()

    def message(self, msg, fg=typer.colors.WHITE, **kwargs):
        s = dt.now()
        timestamp = s.strftime("%H:%M:%S")
        ts_part = typer.style(timestamp, fg=typer.colors.GREEN)
        isbn_part = typer.style(self.isbn, fg=typer.colors.CYAN)
        msg_part = typer.style(msg, fg=fg, bold=True)
        typer.echo(f"[{ts_part} {isbn_part}] {msg_part}", **kwargs)

    async def part1_get_book_ids(self, pylibgen_lib: pylibgen.Library):
        return await pylibgen_lib.search(req=self.isbn, mode="isbn", session=self.session)
    
    async def part2_get_best_book_from_ids(self, pylibgen_lib: pylibgen.Library, book_ids: list[str]):
        return await pylibgen_lib.lookup(ids=book_ids, extension="pdf", session=self.session)
    
    async def part3_download_book(self, libgen_book):
        book = Book.from_libgen_book(libgen_book, isbn=self.isbn)
        return await self._download_book(book=book)

    def elapsed(self, start):
        return round((time.perf_counter() - start), 2)
