from playwright.sync_api import sync_playwright
import re

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/138.0 Safari/537.36"
)


def fetch_home_value(url: str):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=USER_AGENT
        )

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        text = page.locator("body").inner_text()

        browser.close()

    match = re.search(
        r"\$([\d,]+)",
        text
    )

    if not match:
        raise Exception("Unable to locate home value.")

    value = int(
        match.group(1).replace(",", "")
    )

    return value