from app.vesta_art.art_map import art_map
import random
from app.common import helpers


def retrieve_art_layout():
    random_art_index = random.randint(0, len(art_map) - 1)
    random_key = list(art_map.keys())[random_art_index]
    random_value = art_map[random_key]
    # print("Random Key:", random_key)
    # print("Corresponding Value:", random_value)
    return random_value


def vesta_art():
    random_layout = retrieve_art_layout()
    vestaboard_json_body = random_layout
    helpers.post_to_vestaboard(vestaboard_json_body)


# (assets/art-1.png)
# (assets/art-2.png)
# (assets/art-3.png)
# (assets/art-4.png)
# (assets/art-5.png)
# (assets/art-6.png)
# (assets/art-7.png)
# (assets/art-8.png)
# (assets/art-9.png)
# (assets/art-10.png)
# (assets/art-11.png)
# (assets/art-12.png)
# (assets/art-13.png)
# (assets/art-14.png)
# (assets/art-15.png)
# (assets/art-16.png)
# (assets/art-17.png)
# (assets/art-18.png)
# (assets/art-19.png)