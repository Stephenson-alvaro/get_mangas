import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"))
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(5000)  # attendre 5 secondes
        await page.wait_for_load_state("networkidle")
        content = await page.content()
        await browser.close()
    return content

def parse_catalogue(html: str):
    soup = BeautifulSoup(html, "html.parser")
    mangas = []

    for item in soup.select(".bsx"):
        a_tag = item.select_one("a")
        if not a_tag:
            continue
        href = a_tag["href"]
        title = a_tag.get("title", "").strip()
        typename = item.select_one(".typename")
        manga_type = typename.text.strip() if typename else "Unknown"
        img_tag = item.select_one("img")
        img_url = img_tag["src"] if img_tag else ""
        name = item.select_one(".tt")
        name_text = name.text.strip() if name else ""
        volume = item.select_one(".epxs")
        volume_text = volume.text.strip() if volume else ""

        mangas.append({
            "url": href,
            "title": title,
            "type": manga_type,
            "image": img_url,
            "name": name_text,
            "volume": volume_text,
        })
    return mangas

async def main():
    url = "https://sushiscan.net/catalogue/?page=1"
    html = await scrape_page(url)
    mangas = parse_catalogue(html)
    for manga in mangas:
        print(manga)

if __name__ == "__main__":
    asyncio.run(main())
