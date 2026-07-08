from app.thanksgiving.thanksgiving_map import thanksgiving_map
from app.common import helpers
from time import sleep


def thanksgiving_art():
    art_list = [
        "thanksgiving-0",  # (assets/thanksgiving-0.png)
        "thanksgiving-1",  # (assets/thanksgiving-1.png)
        "thanksgiving-2",  # (assets/thanksgiving-2.png)
        "thanksgiving-3",  # (assets/thanksgiving-3.png)
        "thanksgiving-4",  # (assets/thanksgiving-4.png)
        "thanksgiving-5",  # (assets/thanksgiving-5.png)
        "thanksgiving-6",  # (assets/thanksgiving-6.png)
        "thanksgiving-7",  # (assets/thanksgiving-7.png)
    ]

    for art_name in art_list:
        helpers.post_to_vestaboard(thanksgiving_map[art_name])
        sleep(300)
