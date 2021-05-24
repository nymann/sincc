from devtools import debug
from aiohttp_socks import ProxyConnector
from aiohttp.client import ClientSession
import time
import asyncio
import typer
import random
from pathlib import Path
from libgen_dl.config import socks_names, user_agents

from libgen_dl.domain.downloader import BookDownloader

app = typer.Typer()

@app.command()
def main(isbns: list[str], output_dir: Path = Path.cwd()):
    if not output_dir.is_dir():
        raise Exception("Output dir must exist.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(l1(isbns, output_dir))
    loop.close()

async def l1(isbns, path):
    coroutines = []
    start = time.perf_counter()
    for isbn in isbns:
        coroutines.append(BookDownloader().chainer(start, isbn, path))
        #coroutines.append(add(isbn))
        #coroutines.append(request_example(isbn))
    messages = await asyncio.gather(*coroutines)
    debug(messages)

async def add(isbn):
    typer.echo(f"[{isbn}] processing")
    await asyncio.sleep(random.randint(3, 10))
    typer.echo(f"[{isbn}] downloaded")
    return f"[{isbn}] Downloaded some neat book"

def prep_request():
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

async def request_example(isbn):
    proxy, headers = prep_request()
    async with ClientSession(headers=headers, connector=proxy) as session:
        async with session.get("https://nymann.dev/") as response:
            typer.echo(f"[{isbn}] processing")
            await response.text()
            typer.echo(f"[{isbn}] downloaded")
            return f"[{isbn}] Downloaded some neat book"


if __name__ == "__main__":
    app()
