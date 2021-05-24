import random
from datetime import datetime as dt
from devtools import debug
from aiohttp_socks import ProxyConnector
import time
import asyncio
import typer
from pathlib import Path

from libgen_dl.domain.downloader import BookDownloader

app = typer.Typer()

@app.command()
def main(isbns: list[str], output_dir: Path = Path.cwd()):
    if not output_dir.is_dir():
        raise Exception("Output dir must exist.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(l1(isbns, output_dir))
    loop.close()

def regular_task(isbn):
    message(f"CALL: time.sleep(5)", isbn)
    time.sleep(5)
    message("DONE: time.sleep(5)", isbn, fg=typer.colors.GREEN)


async def sleeper(isbn):
    s = random.randint(2,5)
    message(f"CALL: await asyncio.sleep({s})", isbn)
    await asyncio.sleep(s)
    message(f"DONE: asyncio.sleep({s})", isbn, fg=typer.colors.GREEN)
    regular_task(isbn)

def message(msg, isbn, fg=typer.colors.WHITE):
    s = dt.now()
    timestamp = s.strftime("%H:%M:%S")
    ts_part = typer.style(timestamp, fg=typer.colors.GREEN)
    isbn_part = typer.style(isbn, fg=typer.colors.CYAN)
    msg_part = typer.style(msg, fg=fg, bold=True)
    typer.echo(f"[{ts_part} {isbn_part}] {msg_part}")

async def l1(isbns, path):
    coroutines = []
    start = time.perf_counter()
    for isbn in isbns:
        #coroutines.append(BookDownloader().chainer(start, isbn, path))
        coroutines.append(sleeper(isbn))
    await asyncio.gather(*coroutines)


if __name__ == "__main__":
    app()
