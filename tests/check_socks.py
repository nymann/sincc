import requests
from devtools import debug

from libgen_dl.config import socks_names

def test_random_socks():
    for socks_name in socks_names:
        response = requests.get(
            url="https://ifconfig.co",
            proxies={
                "http": f"socks5://{socks_name}.mullvad.net",
                "https": f"socks5://{socks_name}.mullvad.net",
            },
            allow_redirects=True,
            headers={
                #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
                "User-Agent": "curl/7.76.1",
            },
            stream=False,
        )
        #ip: str = response.raw._connection.sock.getpeername()
        debug(socks_name, response.content)


if __name__ == "__main__":
    test_random_socks()
