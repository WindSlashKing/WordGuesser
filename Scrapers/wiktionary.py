import httpx
from bs4 import BeautifulSoup

BASE_URL: str = "https://bg.wiktionary.org/w/index.php?title=Категория:Думи_в_българския_език&from=А"

async def get_html_response(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text

def get_anchors(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("a", href=True)

def parse_next_page_url(html: str) -> str:
    matches = get_anchors(html)
    for match in matches:
        if match.get_text() == "следваща страница":
            return BASE_URL + match["href"]
    raise IndexError("Reached end of pages")
        
def parse_words(html: str) -> set[str]:
    matches = get_anchors(html)

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

async def scrape_wiktionary() -> set[str]:
    client = httpx.AsyncClient()
    html = await get_html_response(client, BASE_URL)
    total_words: set[str] = set()
    while True:
        total_words.update(parse_words(html))
        try:
            next_page_url = parse_next_page_url(html)
        except IndexError:
            break
        html = await get_html_response(client, next_page_url)
    await client.aclose()
    return total_words
