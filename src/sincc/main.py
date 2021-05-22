app = typer.Typer()

@app.command()
def main():
    typer.echo("hello world")


if __name__ == "__main__":
    app()
