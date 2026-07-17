import os

from app.home_value.redfin import fetch_redfin_value
from app.home_value.history import get_previous
from app.home_value.history import save

from app.home_value.formatter import row
from app.common import helpers


PROPERTY_ID = os.environ["PROPERTY_ID"]


def money(value):

    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"

    return f"${value/1000:.1f}K"


def home_value():

    print("Fetching Redfin valuation...")

    result = fetch_redfin_value(
        PROPERTY_ID
    )

    value = result["value"]

    previous = get_previous()

    change = 0

    if previous:

        change = value - previous["value"]

    save(value)


    message = [

        row("HOME VALUE"),

        row(""),

        row(money(value)),

        row("CHANGE"),

        row(
            f"{'+' if change >= 0 else '-'}"
            f"{money(abs(change))}"
        ),

        row("REDFIN UPDATE")
    ]


    helpers.post_to_vestaboard(
        message
    )


if __name__ == "__main__":

    try:

        home_value()

    except Exception as e:

        print(
            f"Home value failed: {e}"
        )

        raise