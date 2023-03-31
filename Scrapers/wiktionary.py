import httpx
from bs4 import BeautifulSoup
import json

BASE_URL: str = "https://bg.wiktionary.org/w/index.php?title=Категория:Думи_в_българския_език&from=А"

async def send_request(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text

def parse_next_page_url(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    matches = soup.find_all("a", href=True)
    for match in matches:
        if match.get_text() == "следваща страница":
            return BASE_URL + match["href"]
    raise IndexError("Reached end of pages")
        
def parse_words(html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    matches = soup.find_all("a", href=True)

    element_words: list[str] = [match.get_text() for match in matches]

    # To remove the letter that we are currently scraping
    element_words.pop(0)

    word_to_split_by = "следваща страница" if "следваща страница" in element_words else "предишна страница"

    # Remove everything before first "word_to_split_by"
    first_split_index = element_words.index(word_to_split_by)
    after_first_split = element_words[first_split_index + 1:]

    # Remove everything after second "word_to_split_by"
    second_split_index = after_first_split.index(word_to_split_by)
    words = set(word.lower() for word in after_first_split[:second_split_index - 1])
    return words

async def scrape_wiktionary():
    client = httpx.AsyncClient()
    html = await send_request(client, BASE_URL)
    total_words: set[str] = set()
    while True:
        total_words.update(parse_words(html))
        try:
            next_page_url = parse_next_page_url(html)
        except IndexError:
            break
        html = await send_request(client, next_page_url)
        print(len(total_words))
    
    with open("dictionary.json", "w", encoding="utf-8") as f:
        json.dump(total_words, f, indent=2, ensure_ascii=False)

    await client.aclose()
