# scrape.py
import asyncio
from playwright.async_api import async_playwright

async def fetch_html(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        print(content)  # Peut être redirigé vers un fichier si besoin
        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scrape.py <URL>")
    else:
        asyncio.run(fetch_html(sys.argv[1]))
