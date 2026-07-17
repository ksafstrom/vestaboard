import requests
import os


def fetch_redfin_value(property_id: str):

    url = (
        "https://www.redfin.com/stingray/api/home/"
        f"details?propertyId={property_id}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return parse_home_value(data)


def parse_home_value(data):

    """
    Redfin response parser.

    Redfin nests property information deeply.
    This keeps the extraction isolated.
    """

    try:

        home_data = data["payload"]["propertyInfo"]

        value = home_data["price"]

        return {
            "value": value
        }

    except KeyError:

        print(data)

        raise Exception(
            "Unable to locate Redfin estimate"
        )