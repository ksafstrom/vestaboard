# daily_pokemon.py
# TO DOs
# Offer for free can not be behind Vestaboard+
# Cache API and/or limit to 151
# Togglable between Ordered and Random
import requests
import random
from app.common import helpers
from app.daily_pokemon.energy_code_map import energy_code_map

print("Opening the Pokedex...")


# Create a function that retrieves the Pokemon data from Kalos

def fetch_pokemon():
    kalos_url = "https://pokeapi.co/api/v2/pokemon/"
    response = requests.get(kalos_url)
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("content-type"))
    print("Response:")
    print(response.text[:500]) 

def fetch_pokemon():
    pokemon_id = random.randint(1, 1025)

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    response = requests.get(url, timeout=10)

    print("Status:", response.status_code)
    print("Response:")
    print(response.text[:500])

    if response.status_code != 200:
        print("Failed to fetch Pokemon")
        return None

    pokemon_data = response.json()

    pokemon_number = pokemon_data.get("id")
    pokemon_name = pokemon_data.get("name", "").title()

    type_list = [
        pokemon["type"]["name"].title()
        for pokemon in pokemon_data["types"]
    ]

    pokemon_type = "/".join(type_list)

    energy_colors = [
        energy_code_map.get(type_name, 69)
        for type_name in type_list
    ]

    height_inches = pokemon_data["height"] * 3.93701

    pokemon_feet = int(height_inches // 12)
    pokemon_inches = int(height_inches % 12)

    pokemon_weight_formatted = "{:.2f}".format(
        pokemon_data["weight"] / 10
    )

    pokemon_abilities = pokemon_data["abilities"][0]["ability"]["name"].title()

    return (
        energy_colors,
        pokemon_name,
        pokemon_number,
        pokemon_type,
        pokemon_feet,
        pokemon_inches,
        pokemon_weight_formatted,
        pokemon_abilities,
    )

        # if kalos_data and isinstance(kalos_data, list) and len(kalos_data) > 0:
        #     random_pokemon_index = random.randint(
        #         0, len(kalos_data)
        #     )  # Numerical value is based on list entry in response
        #     pokemon_number = kalos_data[random_pokemon_index].get("number", None)
        #     pokemon_name = kalos_data[random_pokemon_index].get("name", None)
        #     type_list = [type_name.title() for type_name in kalos_data[random_pokemon_index].get("type", [])]
        #     pokemon_type = "/".join(type_list)
        #     pokemon_feet = int(kalos_data[random_pokemon_index].get("height", None) // 12)  # N // 12 = feet
        #     pokemon_inches = int(kalos_data[random_pokemon_index].get("height", None) % 12)  # N % 12 = inches
        #     if pokemon_inches <= 10:  # Less than equal to 10 add zero before value
        #         pokemon_inches = "0" + str(pokemon_inches)
        #     else:
        #         pokemon_inches
        #     pokemon_weight = kalos_data[random_pokemon_index].get("weight", None)
        #     if pokemon_weight >= 9999:  # Greater than or equal to account for Gigantimax Evolutions
        #         pokemon_weight_formatted = "????.?"
        #     else:
        #         pokemon_weight_formatted = "{:.2f}".format(pokemon_weight)
        #     pokemon_abilities = kalos_data[random_pokemon_index].get("abilities", [])
        #     pokemon_abilities = next(ability for ability in pokemon_abilities if ability is not None)
        #     # print(f"Pokedex Entry: {pokemon_name}, {pokemon_number}, {pokemon_type}, {pokemon_height:.2f}, {pokemon_weight:.2f}, {pokemon_abilities}")
        #     energy_colors = [energy_code_map.get(type_name, 69) for type_name in type_list]
        #     return (
        #         energy_colors,
        #         pokemon_name,
        #         pokemon_number,
        #         pokemon_type,
        #         pokemon_feet,
        #         pokemon_inches,
        #         pokemon_weight_formatted,
        #         pokemon_abilities,
        #     )


# TODO look into writing logic for orientation: str,
def translate_names(inputstring: str, expected_length: int):
    character_result = helpers.convert_string_character_code(inputstring)
    if len(character_result) == expected_length:
        return character_result

    # If we are here string manipulation is needed.
    if len(character_result) > expected_length:
        return character_result[:expected_length]

    numberofpadding = expected_length - len(character_result)

    for _ in range(numberofpadding):
        character_result.append(0)

    return character_result


def daily_pokemon():
    # Break the translate_to_name_character_codes into two different functions for alpha characters compared to numerical a thrid would be required for color.
    (
        energy_colors,
        pokemon_name,
        pokemon_number,
        pokemon_type,
        pokemon_feet,
        pokemon_inches,
        pokemon_weight_formatted,
        pokemon_abilities,
    ) = fetch_pokemon()
    name_characters = helpers.account_for_padding(pokemon_name, 12, False)
    number_characters = helpers.account_for_padding(pokemon_number, 4, True)
    type_characters = translate_names(pokemon_type, 15)
    height_characters = helpers.left_align_padding(f"{pokemon_feet}'{pokemon_inches}\"", 7)
    weight_characters = helpers.left_align_padding(f"{pokemon_weight_formatted} LBS", 10)
    abilities_characters = translate_names(
        pokemon_abilities, 16
    )  # Longest known abilities is 16 characters, edge case.  Need to make the word ability shorter or abberivated to make space.
    energy_character = [energy_colors[0], energy_colors[-1], energy_colors[0], energy_colors[-1]]
    energy_character_2 = [energy_colors[-1], energy_colors[0], energy_colors[-1], energy_colors[0]]

    vestaboard_json_body = [
        [*energy_character, 0, *name_characters, 0, *energy_character],
        [*energy_character_2, 0, 0, 0, 0, 39, *number_characters, 0, 0, 0, 0, 0, *energy_character_2],
        [20, 25, 16, 5, 50, 0, *type_characters, 0],
        [0, 1, 2, 12, 50, 0, *abilities_characters],
        [0, 0, 8, 20, 50, 0, *height_characters, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 23, 20, 50, 0, *weight_characters, 0, 0, 0, 0, 0, 0],
    ]
    print("Creating message...")
    helpers.post_to_vestaboard(vestaboard_json_body)
    print("Message sent!")

if __name__ == "__main__":
    try:
        daily_pokemon()
    except Exception as e:
        print(f"Daily Pokemon failed: {e}")
        raise
