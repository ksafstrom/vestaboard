import json
import os

FILE = "home_value.json"


def get_previous():

    if not os.path.exists(FILE):
        return None

    with open(FILE) as f:
        return json.load(f)


def save(value):

    with open(FILE, "w") as f:

        json.dump(
            {
                "value": value
            },
            f
        )