from flask import Blueprint, render_template
from datetime import timedelta
import arrow
import json
import requests


views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/arrows")
def arrows():
    with open("data.json", "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
    # sunset_sunrise_api = data['sunset_sunrise_api'].split("{}")
    ipgeolocation_api = data['ipgeolocation_api'].split("{}")
    print(ipgeolocation_api)
    dates = data['dates']
    results = {}
    for date in dates:
        # url = f"{sunset_sunrise_api[0]}{data['latitude']}{sunset_sunrise_api[1]}{data['longitude']}{sunset_sunrise_api[2]}{date}"
        url = f"{ipgeolocation_api[0]}{data['ipgeolocation_api_tokens'][0]}{ipgeolocation_api[1]}{data['latitude']}{ipgeolocation_api[2]}{data['longitude']}{ipgeolocation_api[3]}{date}"
        print(url)
        result = requests.get(url)
        results[date] = result.json()
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    return results


@views.route("/weather", methods=["GET", "POST"])
def weather():
    with open("key.txt", "r") as file:
        keys = file.readlines()
    keys = [key.split("\n")[0] for key in keys]
    json_data = []
    start = arrow.Arrow(2021, 10, 1, 12)
    end = arrow.Arrow(2021, 10, 1, 12)
    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': 68.9876975,
            'lng': 40.9483998,
            'params': ",".join(keys),
            'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
        },
        headers={
            'Authorization': '155644c8-50e4-11ec-b247-0242ac130002-15564540-50e4-11ec-b247-0242ac130002'
        }
    )
    json_data.append(response.json())
    for i in range(3):
        start += timedelta(10)
        end += timedelta(10)
        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat': 68.9876975,
                'lng': 40.9483998,
                'params': ",".join(keys),
                'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
                'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
            },
            headers={
                'Authorization': '155644c8-50e4-11ec-b247-0242ac130002-15564540-50e4-11ec-b247-0242ac130002'
            }
        )
        json_data.append(response.json())
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file)
    return {'success': True}
