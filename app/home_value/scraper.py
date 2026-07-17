from playwright.sync_api import sync_playwright


def fetch_home_value(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        page.screenshot(path="debug.png", full_page=True)

        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        with open("debug.txt", "w", encoding="utf-8") as f:
            f.write(page.locator("body").inner_text())

        browser.close()

    raise Exception("Debug complete.")