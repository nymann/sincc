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
    for isbn in isbns:
        coroutines.append(BookDownloader(isbn=isbn, output_dir=path).chainer())
    await asyncio.gather(*coroutines)

if __name__ == "__main__":
    app()
