from app.common import helpers
from app.common.character_code_map import character_code_map
from app.vesta_christmas.christmas_map import christmas_map
from time import sleep
import datetime


def christmas_timer():
    # Get the current day and year
    today = datetime.date.today()
    year = today.year
    xmas = datetime.date(year, 12, 25) - datetime.date.today()
    xmas_days = str(xmas.days)
    if len(xmas_days) == 2:
        xmas_days = " " + xmas_days  # one space added in front of number
    if len(xmas_days) == 1:
        xmas_days = "  " + xmas_days  # two spaces added in front of number

    xmas_characters = helpers.convert_string_character_code(xmas_days)
    print(xmas_characters)

    # Vestaboard Response
    vestaboard_json_body = [
        [0, 0, 0, 3, 15, 21, 14, 20, 4, 15, 23, 14, 0, 21, 14, 20, 9, 12, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 8, 18, 9, 19, 20, 13, 1, 19, 0, 0, 0, 0, 0, 0, 0],
        [63, 66, 63, 66, 63, 66, 63, 66, 63, 66, 63, 66, 63, 66, 63, 66, 63, 66, 63, 66, 63, 66],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, *xmas_characters, 0, 4, 1, 25, 19, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    helpers.post_to_vestaboard(vestaboard_json_body)
    sleep(630)


# def christmas_art():
#     art_list = [
#         "christmas-0", #(assets/christmas-0.png)
#         "christmas-1", #(assets/christmas-1.png)
#         "christmas-2", #(assets/christmas-2.png)
#         "christmas-3", #(assets/christmas-3.png)
#         "christmas-4", #(assets/christmas-4.png)
#         "christmas-5", #(assets/christmas-5.png)
#         "christmas-6", #(assets/christmas-6.png)
#         "christmas-7", #(assets/christmas-7.png)
#         "christmas-8", #(assets/christmas-8.png)
#     ]

#     for art_name in art_list:
#         helpers.post_to_vestaboard(christmas_map[art_name])
#         sleep(300)
