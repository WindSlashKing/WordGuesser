import string

import httpx
from bs4 import BeautifulSoup

BASE_URL: str = "https://slovored.com"
BASE_URLS: list[str] = [
    "https://slovored.com/sitemap/polytechnical",
    "https://slovored.com/sitemap/geography",
    "https://slovored.com/sitemap/medical",
    "https://slovored.com/sitemap/synonymous",
    "https://slovored.com/sitemap/unilingual",
    "https://slovored.com/sitemap/pravopisen-rechnik",
    "https://slovored.com/sitemap/grammar"
]

BULGARIAN_ALPHABET: str = "абвгдежзийклмнопрстуфхцчшщъьюя"
ENGLISH_ALPHABET: str = string.ascii_lowercase

async def get_html_response(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text

def get_anchors(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("a", href=True)

def parse_words(html: str) -> set[str]:
    matches = get_anchors(html)
    words: set[str] = set()
    start_adding = False
    for match in matches:
        if match.get_text() == "Политика на бисквитки":
            start_adding = True
            continue
        if start_adding:
            words.add(match.get_text())
    return words

def parse_sublinks_from_english_page(html: str) -> set[str]:
    matches = get_anchors(html)
    sublinks: set[str] = set()

    bulgarian_words_text_element_index = html.index("Български думи")

    for match in matches:
        if html.index(match["href"]) < bulgarian_words_text_element_index:
            continue
        # Using [0:] to remove a double backslash
        sublinks.add(BASE_URL + match["href"][0:])

    return sublinks

def parse_sublinks(html: str) -> set[str]:
    matches = get_anchors(html)
    sublinks: set[str] = set()

    for match in matches:
        if "letter" not in match["href"]:
            continue
        # Using [0:] to remove a double backslash
        sublinks.add(BASE_URL + match["href"][0:]) 

    return sublinks

async def parse_initial_links() -> set[str]:
    scraped_links: set[str] = set()
    async with httpx.AsyncClient() as client:
        for index, link in enumerate(BASE_URLS):
            html = await get_html_response(client, link)
            if index < 3:
                scraped_links.update(parse_sublinks_from_english_page(html))
                continue
            scraped_links.update(parse_sublinks(html))
    return scraped_links

all_scraped_links: set[str] = set()
async def recursively_parse_links(client: httpx.AsyncClient, links: set[str]):
    if not links:
        return
    for link in links.copy():
        html = await get_html_response(client, link)
        new_links = parse_sublinks(html)
        all_scraped_links.update(new_links)
        await recursively_parse_links(client, new_links)

async def scrape_slovored() -> set[str]:
    all_scraped_links.update(await parse_initial_links())
    client = httpx.AsyncClient()
    await recursively_parse_links(client, all_scraped_links)
    total_words: set[str] = set()
    for link in all_scraped_links:
        html = await get_html_response(client, link)
        total_words.update(parse_words(html))
    await client.aclose()
    return total_words