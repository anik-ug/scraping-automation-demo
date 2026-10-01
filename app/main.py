import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

from .config import SETTINGS
from .scraper import Scraper


async def run():
    print("=" * 65)
    print("SCRAPING & BROWSER AUTOMATION DEMO")
    print("Anik Kumar | 30 September 2026")
    print("=" * 65)
    print(f"Target: {SETTINGS.target_url}")
    print(f"Concurrent workers: {SETTINGS.workers}")
    print("Retry demo: one intentionally invalid task is included.")
    print()

    urls = [
        SETTINGS.target_url,
        SETTINGS.target_url,
        SETTINGS.target_url,
        SETTINGS.target_url,
        "http://127.0.0.1:8000/this-route-does-not-exist",
    ]

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        scraper = Scraper(browser)

        tasks = [
            scraper.scrape(url, worker_id=i + 1, task_id=i + 1)
            for i, url in enumerate(urls)
        ]

        results = await asyncio.gather(*tasks)

        await browser.close()

    output = {
        "run": {
            "workers": SETTINGS.workers,
            "tasks": len(tasks),
            "target": SETTINGS.target_url,
        },
        "results": results,
    }

    Path("results.json").write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 65)
    print("BATCH COMPLETE")
    print("=" * 65)
    print(json.dumps(output, indent=2))
    print("\nSaved: results.json")


if __name__ == "__main__":
    asyncio.run(run())
