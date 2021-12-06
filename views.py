from arrow import Arrow
from flask import Blueprint, render_template
from datetime import timedelta
import json
import requests


views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/")
def index():
    return render_template("index.html")


# @views.route("/arrows")
# def arrows():
#     with open("data.json", "r", encoding="UTF-8") as file:
#         data = json.loads(file.read())
#     # sunset_sunrise_api = data['sunset_sunrise_api'].split("{}")
#     ipgeolocation_api = data['ipgeolocation_api'].split("{}")
#     print(ipgeolocation_api)
#     dates = data['dates']
#     results = {}
#     for date in dates:
#         # url = f"{sunset_sunrise_api[0]}{data['latitude']}{sunset_sunrise_api[1]}{data['longitude']}{sunset_sunrise_api[2]}{date}"
#         url = f"{ipgeolocation_api[0]}{data['ipgeolocation_api_tokens'][0]}{ipgeolocation_api[1]}{data['latitude']}{ipgeolocation_api[2]}{data['longitude']}{ipgeolocation_api[3]}{date}"
#         print(url)
#         result = requests.get(url)
#         results[date] = result.json()
#     with open("results.json", "w", encoding="utf-8") as file:
#         json.dump(results, file, ensure_ascii=False, indent=4)
#     return results


@views.route("/weather", methods=["GET", "POST"])
def weather():
    with open("data.json", "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
    dates = data['dates']
    with open("key.txt", "r") as file:
        keys = [key.split("\n")[0] for key in file.readlines()]
    json_data = {}
    token_index = 0
    for date in dates:
        current_date = date['date'].split("-")
        year = int(current_date[0])
        month = int(current_date[1])
        day = int(current_date[2])
        sunrise_time = date['sunrise'].split(":")
        sunrise_hour = int(sunrise_time[0]) + 1
        sunset_time = date['sunset'].split(":")
        sunset_hour = int(sunset_time[0])
        start = Arrow(year, month, day, sunrise_hour)
        end = Arrow(year, month, day, sunset_hour)
        json_data[date['date']] = {
            'start': start.__str__(),
            'end': end.__str__()
        }
        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat': data['latitude'],
                'lng': data['longitude'],
                'params': ",".join(keys),
                'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
                'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
            },
            headers={
                'Authorization': data['stormglass_api_tokens'][token_index]
            }
        )
        print(response.json())
        json_data[date['date']] = response.json()
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    return json_data
