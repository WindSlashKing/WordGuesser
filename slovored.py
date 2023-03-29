import httpx
from bs4 import BeautifulSoup
import json
import string

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

async def send_request(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text

def parse_words(html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    matches = soup.find_all("a", href=True)
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
    soup = BeautifulSoup(html, "html.parser")
    matches = soup.find_all("a", href=True)
    sublinks: set[str] = set()
    if "Български думи" not in html:
        print(html)
    bulgarian_words_text_element_index = html.index("Български думи")
    for match in matches:
        if html.index(match["href"]) < bulgarian_words_text_element_index:
            continue
        # Using [0:] to remove a double backslash
        sublinks.add(BASE_URL + match["href"][0:])

    return sublinks

def parse_sublinks(html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    matches = soup.find_all("a", href=True)
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
            html = await send_request(client, link)
            if index < 3:
                scraped_links.update(parse_sublinks_from_english_page(html))
                continue
            scraped_links.update(parse_sublinks(html))
    return scraped_links

all_scraped_links: set[str] = set()
async def recursively_parse_links(links: set[str]):
    if len(links) == 0:
        return
    async with httpx.AsyncClient() as client:
        for link in links.copy():
            html = await send_request(client, link)
            new_links = parse_sublinks(html)
            all_scraped_links.update(new_links)
            await recursively_parse_links(new_links)

async def scrape_slovored():
    all_scraped_links.update(await parse_initial_links())
    await recursively_parse_links(all_scraped_links)
    print(len(all_scraped_links))

    total_words: set[str] = set()
    async with httpx.AsyncClient() as client:
        for link in all_scraped_links:
            html = await send_request(client, link)
            total_words.update(parse_words(html))
    with open("slovored.json", "w", encoding="utf-8") as f:
        json.dump(list(total_words), f, indent=2, ensure_ascii=False)