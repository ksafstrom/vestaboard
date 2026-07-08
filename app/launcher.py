import argparse


# from app.op_tourney import op_tourney
from app.vesta_st_patricks import vesta_st_patricks
from app.thanksgiving import thanksgiving
from app.vesta_art import vesta_art
from app.daily_pokemon import daily_pokemon
from app.vesta_christmas import vesta_christmas
from app.common import helpers
from time import sleep

# python launcher.py [app_name] [--sandbox]


# Runs the Daily Pokemon
def run_daily_pokemon():
    daily_pokemon.daily_pokemon()


# Runs St. Patrick's Thematic Art
def run_stpaddys():
    previous_board_message = helpers.get_from_vestaboard()
    vesta_st_patricks.stpaddys_art()
    # finally reset what was there before
    helpers.post_to_vestaboard(previous_board_message)


# Runs Thanksgiving Thematic Art
def run_thanksgiving():
    previous_board_message = helpers.get_from_vestaboard()
    thanksgiving.thanksgiving_art()
    # finally reset what was there before
    helpers.post_to_vestaboard(previous_board_message)

# Runs Vest Art
def run_vesta_art():
    vesta_art.vesta_art()


# Runs Christmas Countdown Timer and Thematic Art
def run_vesta_christmas():
    previous_board_message = helpers.get_from_vestaboard()
    vesta_christmas.christmas_timer()
    sleep(300)
    # vesta_christmas.christmas_art()
    helpers.post_to_vestaboard(previous_board_message)


# List of applicable applications
APPS = {
    "daily_pokemon": run_daily_pokemon,
    "vesta_st_patricks": run_stpaddys,
    "thanksgiving": run_thanksgiving,
    "vesta_art": run_vesta_art,
    "vesta-christmas": run_vesta_christmas,
}

# Arguements for launching apps
def main():
    parser = argparse.ArgumentParser(description="Launcher for the various Vestaboard Apps")
    parser.add_argument(
        "app",
        choices=[
            "daily_pokemon",
            "vesta_st_patricks",
            "thanksgiving",
            "vesta_art",
            "vesta-christmas",
        ],
        help="Specify the app to run",
    )
    parser.add_argument("--sandbox", action="store_true", help="Determine if we post to sandbox or real vestaboard")
    args = parser.parse_args()
    helpers.POST_TO_SANDBOX = args.sandbox
    APPS[args.app]()


if __name__ == "__main__":
    main()
