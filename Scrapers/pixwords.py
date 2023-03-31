import httpx
from bs4 import BeautifulSoup
import json

def get_pages_urls() -> set[str]:
    return set(f"https://pixwords-help.info/bg/?all&page={i}" for i in range(1, 67))
    
async def get_html_responses(urls: set[str]) -> set[str]:
    html_responses: set[str] = set()
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.get(url)
            html = response.text
            html_responses.add(html)
    return html_responses

def parse_all_words(html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    matches = soup.find_all("span")
    words: set[str] = set()
    for match in matches:
        element_text: str = match.get_text()
        if not element_text.isalpha():
            continue
        if "търсене" in element_text.lower():
            continue
        words.add(element_text)
    return words

async def scrape_pixwords() -> set[str]:
    urls = get_pages_urls()
    html_responses = await get_html_responses(urls)
    words: set[str] = set()
    for html_response in html_responses:
        words.update(parse_all_words(html_response))
    return words