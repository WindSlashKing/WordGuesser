import asyncio
import json

import pixwords

def combine_jsons(*files) -> None:
    content = set()
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content.update(json.load(f))
    with open("combined.json", "w", encoding="utf-8") as f:
        json.dump(sorted(content), f, ensure_ascii=False, indent=2, sort_keys=True)

async def main():
    combine_jsons("all_bulgarian_words.json", "pixwords.json")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())