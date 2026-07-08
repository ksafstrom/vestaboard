# Ability Length Script
import requests

kalos_api = requests.get("https://www.pokemon.com/us/api/pokedex/kalos").json()

current_max = 0
current_max_ability = ""
for pokemon in kalos_api:
    for ability in pokemon["abilities"]:
        if current_max < len(ability):
            current_max = len(ability)
            current_max_ability = ability

print(current_max_ability, current_max)

# List of 16 character Abilities:
# Koffing Neutralizing Gas
# Weezing Neutralizing Gas
# Slowking Curious Medicine
# Darmanitan Gorilla Tactics
# Yamask Wandering Spirit
# Zygarde Power Construct
# Tsareena Queenly Majesty
# Sandygast Water Compaction
# Palossand Water Compaction
# Solgaleo Full Metal Body
# Runerigus Wandering Spirit
# Zamazenta Dauntless Shield
# Oinkologne Lingering Aroma
# Dachsbun Well-Baked Body
# Bellibolt Electromorphosis
# Kingambit Supreme Overlord
# Frigibax Thermal Exchange
# Arctibax Thermal Exchange
# Baxcalibur Thermal Exchange
# Wo-Chien Tablets of Ruin
# Koraidon Orichalcum Pulse
# Dipplin Supersweet Syrup
# Hydrapple Supersweet Syrup
# Pecharunt Poison Puppeteer
