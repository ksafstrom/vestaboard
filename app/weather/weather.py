import os
import requests
from datetime import datetime
from app.common import helpers
from app.weather.forecast_types import forecast_types

print("Opening the forecast...")

CITY = "Seattle, Washington"

# Create a function that retrieves the local weather
def fetch_weather():
    api_key =os.environ["VESTABOARD_WEATHER_KEY"]
    
    url = (
        f"https://api.weatherapi.com/v1/forecast.json"
        f"?key={api_key}"
        f"&q={CITY}"
        "&days=1")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    print("Status:", response.status_code)
    print("Response:")
    print(response.text[:500])

    if response.status_code != 200:
        print("Failed to fetch weather")
        return None
    
    weather_data = response.json()
  
    forecast = weather_data["forecast"]["forecastday"][0]
    date = datetime.strptime(
        forecast["date"],
        "%Y-%m-%d"
    )
    day_of_week = date.strftime("%A")
    month_abb = date.strftime("%b")
    date_number = str(date.day)
    weather_type = forecast_types.get(
    forecast["day"]["condition"]["text"],"WEATHER")
    high_temp = f"{round(forecast['day']['maxtemp_f'])}"
    lo_temp = f"{round(forecast['day']['mintemp_f'])}"

    return (
        day_of_week,
        month_abb,
        date_number,
        weather_type,
        high_temp,
        lo_temp,
    )

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


def weather():
    (
        day_of_week,
        month_abb,
        date_number,
        weather_type,
        high_temp,
        lo_temp,
    ) = fetch_weather()
    print(type(high_temp), high_temp)
    print(type(lo_temp), lo_temp)
    print(type(weather_type), weather_type)
    date = translate_names(date_number, 2)
    month = translate_names(month_abb, 3)
    day = translate_names(day_of_week, 9)
    forecast = translate_names(weather_type, 8)
    high_temp = translate_names(high_temp, 2)
    lo_temp = translate_names(lo_temp, 2)
 

    vestaboard_json_body = [
        [63,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0,63],
        [63,*day, 0, *month, 0, *date, 63,65,67,66,0,63,65],
        [65,*forecast,0,*lo_temp, 44, *high_temp,62,67,66,0,63,65,67],
        [67,66,0,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0,63,65,67,66],
        [66,0,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0],
        [0,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0,63,65,67,66,0,63]
    ]

    print("Creating message...")
    for i, row in enumerate(vestaboard_json_body):print(f"Row {i}: {len(row)}")
    helpers.post_to_vestaboard(vestaboard_json_body)
    print("Message sent!")

if __name__ == "__main__":
    try:
        weather()
    except Exception as e:
        print(f"Weather deployment failed: {e}")
        raise
