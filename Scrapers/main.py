import asyncio
import json

def save_words(words, filename: str) -> None:
    filename = filename if not filename.endswith(".json") else filename + ".json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(list(words), f, indent=2, ensure_ascii=False)

def combine_jsons(*files) -> None:
    content = set()
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content.update(json.load(f))
    with open("combined.json", "w", encoding="utf-8") as f:
        json.dump(sorted(content), f, ensure_ascii=False, indent=2, sort_keys=True)

async def main():
    import pixwords
    import wiktionary
    import slovored
    await pixwords.scrape_pixwords()
    await wiktionary.scrape_wiktionary()
    await slovored.scrape_slovored()

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())