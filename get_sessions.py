import asyncio
import json
from playwright.async_api import async_playwright


async def navegador_com_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Carregar cookies da sessão logada
        cookies = json.load(open("twitch_cookies.json"))
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto("https://www.twitch.tv")

        await page.wait_for_timeout(50000)  # tempo pra confirmar se tá logado
        await browser.close()

asyncio.run(navegador_com_cookies())
