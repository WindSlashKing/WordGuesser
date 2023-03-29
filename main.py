import asyncio
import json

def combine_jsons(*files):
    file_one, file_two = files
    elements = set()
    with open(file_one, "r", encoding="utf-8") as f:
        elements.update(json.load(f))
    with open(file_two, "r", encoding="utf-8") as f:
        elements.update(json.load(f))
    with open("combined.json", "w", encoding="utf-8") as f:
        json.dump(sorted(elements), f, ensure_ascii=False, indent=2, sort_keys=True)

async def main():
    combine_jsons("slovored.json", "words_wiktionary.json")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())