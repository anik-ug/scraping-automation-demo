import asyncio
from playwright.async_api import Browser

from .config import SETTINGS
from .proxy_manager import ProxyManager
from .retry import with_retry
from .session_manager import SessionManager


class Scraper:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.proxy_manager = ProxyManager()
        self.session_manager = SessionManager()

    async def scrape(self, url: str, worker_id: int, task_id: int) -> dict:
        proxy = self.proxy_manager.next_proxy()
        session_id = f"session-{worker_id:02d}"

        async def operation():
            context = await self.session_manager.create_session(
                self.browser, session_id
            )

            try:
                page = await context.new_page()

                print(
                    f"[Worker-{worker_id}] "
                    f"Session={session_id} Proxy={proxy.name} "
                    f"Task={task_id}"
                )

                await asyncio.sleep(SETTINGS.rate_limit_seconds)
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=SETTINGS.timeout_ms,
                )

                items = await page.locator("[data-product]").evaluate_all(
                    """els => els.map(el => ({
                        id: el.dataset.id,
                        name: el.querySelector('.name')?.textContent?.trim(),
                        price: el.querySelector('.price')?.textContent?.trim(),
                        available: el.querySelector('.availability')?.textContent?.trim()
                    }))"""
                )

                return {
                    "url": url,
                    "worker_id": worker_id,
                    "session_id": session_id,
                    "proxy": proxy.name,
                    "status": "success",
                    "items": items,
                }
            finally:
                await context.close()

        try:
            return await with_retry(
                operation,
                SETTINGS.max_retries,
                worker_id,
                task_id,
            )
        except Exception as exc:
            return {
                "url": url,
                "worker_id": worker_id,
                "session_id": session_id,
                "proxy": proxy.name,
                "status": "failed",
                "error": str(exc),
            }
