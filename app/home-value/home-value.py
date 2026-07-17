import os

from app.home_value.scraper import fetch_home_value
from app.home_value.history import load_previous
from app.home_value.history import save
from app.home_value.formatter import row

from app.common import helpers


def format_money(value):

    if value >= 1000000:

        return f"${value/1000000:.2f}M"

    return f"${value/1000:.1f}K"


def home_value():

    value = fetch_home_value(
        os.environ["HOME_URL"]
    )

    previous = load_previous()

    change = 0

    if previous:

        change = value - previous["value"]

    save(value)

    board = [

        row("HOME VALUE"),

        row(""),

        row(format_money(value)),

        row(f"CHANGE"),

        row(format_money(change)),

        row("UPDATED")
    ]

    helpers.post_to_vestaboard(board)


if __name__ == "__main__":

    home_value()