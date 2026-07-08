from app.vesta_st_patricks.st_patricks_map import st_patricks_map
from app.common import helpers
from time import sleep


def stpaddys_art():
    art_list = [
        "stpaddys-0",  # (assets/st_paddys-0.png)
        "stpaddys-1",  # (assets/st_paddys-1.png)
        "stpaddys-2",  # (assets/st_paddys-2.png)
        "stpaddys-3",  # (assets/st_paddys-3.png)
    ]

    for art_name in art_list:
        helpers.post_to_vestaboard(st_patricks_map[art_name])
        sleep(300)
