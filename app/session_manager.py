from playwright.async_api import Browser, BrowserContext


class SessionManager:
    async def create_session(self, browser: Browser, session_id: str) -> BrowserContext:
        context = await browser.new_context(
            locale="en-IN",
            viewport={"width": 1280, "height": 800},
        )
        return context
