import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio


async def scrape_all_cards_html(tags: List[str]) -> List[str]:
    tag_url = "-".join(tag.lower() for tag in tags)
    url = f"https://www.twitch.tv/directory/all/tags/{tag_url}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        await page.wait_for_selector('article[data-a-target^="card-"]', timeout=20000)

        print("⏬ Rolando até carregar todos os cards...")
        prev_count = -1
        scroll_attempts = 0

        while True:
            cards = await page.query_selector_all('article[data-a-target^="card-"]')
            curr_count = len(cards)

            if curr_count == prev_count:
                scroll_attempts += 1
                if scroll_attempts >= 3:
                    break
            else:
                scroll_attempts = 0

            prev_count = curr_count
            await page.mouse.wheel(0, 3000)
            await page.wait_for_timeout(1500)

        print(f"\n✅ Total de cards carregados: {curr_count}\n")

        all_html = []
        for i, card in enumerate(tqdm_asyncio(cards, desc="📦 Extraindo lives")):
            try:
                html = await card.inner_html()
                all_html.append(html)
            except Exception as e:
                print(f"⚠️ Erro ao extrair card {i+1}: {e}")

        await browser.close()
        return all_html


async def extract_live_data_from_html(html: str) -> Dict:
    soup = BeautifulSoup(html, 'html.parser')

    wrapper = soup.find("div", class_="ScTextWrapper-sc-10mto54-1 REkcH")
    if not wrapper:
        return {"error": "Wrapper não encontrado"}

    title_tag = wrapper.find("h3")
    title = title_tag.get_text(
        strip=True) if title_tag else "Título não encontrado"

    user_tag = wrapper.select_one('p.CoreText-sc-1txzju1-0.gBknDX')
    user_name = user_tag.get_text(
        strip=True) if user_tag else "Usuário não encontrado"

    game_tag = wrapper.select_one('a[data-a-target="preview-card-game-link"]')
    game_name = game_tag.get_text(
        strip=True) if game_tag else "Jogo não encontrado"

    tag_spans = wrapper.select('button.tw-tag span')
    tags = [span.get_text(strip=True) for span in tag_spans]

    return {
        "user_name": user_name,
        "title": title,
        "game": game_name,
        "tags": tags
    }


async def main():
    html_list = await scrape_all_cards_html(["VtuberBR"])
    data = []

    print("\n📊 Processando dados das lives...\n")
    for i, html in enumerate(tqdm_asyncio(html_list, desc="🧠 Extraindo dados")):
        live_data = await extract_live_data_from_html(html)
        data.append(live_data)

    print("\n🎉 Extração finalizada!")
    print(f"🔢 Total de lives processadas: {len(data)}")
    for d in data:
        print(f"✅ {d['user_name']} — {d['game']} - {d['tags']}")

asyncio.run(main())
