from bs4 import BeautifulSoup

def test_extract_url():
    content = ""
    with open("tests/example.html", "r") as html_file:
        content = html_file.read()
    
    soup = BeautifulSoup(content)
    anchor_tag = soup.select_one("div#download h2 a[href]")
    href = anchor_tag["href"]
    assert "http://31.42.184.140/main/2294000/59d9309e6ee8107844bcfe6e4bdc6c2e/%28Addison-Wesley%20Object%20Technology%20Series%29%20Martin%20Fowler%20-%20Refactoring_%20Improving%20the%20Design%20of%20Existing%20Code-Addison-Wesley%20Professional%20%282018%29.pdf" == href
