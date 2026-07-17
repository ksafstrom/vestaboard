import json
import os

FILE = "home_value_history.json"


def load_previous():

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
            f,
            indent=4
        )