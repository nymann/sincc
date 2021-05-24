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

async def l1(isbns, path):
    coroutines = []
    start = time.perf_counter()
    for isbn in isbns:
        coroutines.append(BookDownloader().chainer(start, isbn, path))
    await asyncio.gather(*coroutines)

if __name__ == "__main__":
    app()
