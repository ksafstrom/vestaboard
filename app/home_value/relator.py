import json
import re
from playwright.sync_api import sync_playwright


def fetch_redfin_value(url: str):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "Chrome/120 Safari/537.36"
            )
        )

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        html = page.content()

        browser.close()


    return extract_value(html)


def extract_value(html):

    """
    Search Redfin's embedded application state.
    """

    patterns = [

        r'"estimatedValue":(\d+)',

        r'"redfinEstimate":(\d+)',

        r'"price":(\d+)',

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            html
        )

        if match:

            return {
                "value": int(
                    match.group(1)
                )
            }


    raise Exception(
        "Unable to find Redfin estimate"
    )