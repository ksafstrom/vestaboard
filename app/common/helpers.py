# helpers.py
import json
import requests
import os
import urllib3
from app.common.character_code_map import character_code_map

POST_TO_SANDBOX = False

def get_from_vestaboard():
    vestaboard_api_url = "https://rw.vestaboard.com"
    api_key_header_name = "X-Vestaboard-Read-Write-Key"
    api_key_value = os.getenv("VESTABOARD_RW_KEY")
    if not api_key_value:
            raise ValueError("Environment variable VESTABOARD_RW_KEY is missing or empty")

    headers = {
        api_key_header_name: api_key_value
    }

    response = requests.get(
        vestaboard_api_url,
        headers=headers,
        verify=True,
        timeout=30,
    )

    response.raise_for_status()

    current_message = response.json().get("currentMessage", {})
    vestaboard_json_body = json.loads(current_message.get("layout", "[]"))

    print("Current board message.", vestaboard_json_body)
    return vestaboard_json_body


# Posts to the physical or sandbox board based on debug value
def post_to_vestaboard(vestaboard_json_body):
    for line in vestaboard_json_body:
        print(line, len(line))

    vestaboard_api_url = "https://rw.vestaboard.com"

    api_key =  os.getenv(
        "VESTABOARD_SANDBOX_RW_KEY" if POST_TO_SANDBOX else "VESTABOARD_RW_KEY"
    )

    headers = {
        "X-Vestaboard-Read-Write-Key": api_key
    }

    try:
        response = requests.post(
            vestaboard_api_url,
            json=vestaboard_json_body,
            headers=headers,
            verify=True,
            timeout=30,
        )

        print(response.status_code)
        response.raise_for_status()

        if response.content:
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Failed to post to Vestaboard: {e}")
        if "response" in locals() and response is not None:
            print(f"Response status: {response.status_code}")
            print(response.text)

    print(vestaboard_json_body)


# Variable to Vestaboard character conversion
def convert_string_character_code(inputstring):
    character_result = list()
    inputstring = str(inputstring).upper()

    for character in inputstring:
        character_code = character_code_map.get(character)  # from character_code_map.py
        if character_code is not None:
            character_result.append(character_code)
    return character_result


# Assists with transformations and padding
def account_for_padding(inputstring: str, expected_length: int, isnumber: bool):
    character_result = convert_string_character_code(inputstring)
    if len(character_result) == expected_length:
        return character_result

    # If we are here string manipulation is needed.
    if len(character_result) > expected_length:
        return character_result[:expected_length]

    numberofpadding = expected_length - len(character_result)

    if isnumber:
        for _ in range(numberofpadding):
            character_result.insert(0, 0)
        return character_result

    if numberofpadding % 2 == 1:  # Means number of padding is odd
        character_result.insert(0, 0)
        numberofpadding -= 1

    for _ in range(numberofpadding // 2):  # To avoid running multiple times divide by 2
        character_result.insert(0, 0)
        character_result.append(0)

    return character_result


# Daily Pokemon left aligning
def left_align_padding(inputstring: str, expected_length: int):
    character_result = convert_string_character_code(inputstring)
    if len(character_result) == expected_length:
        return character_result

    # If we are here string manipulation is needed.
    if len(character_result) > expected_length:
        return character_result[:expected_length]

    numberofpadding = expected_length - len(character_result)

    for _ in range(numberofpadding):
        character_result.append(0)

    return character_result
