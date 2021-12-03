from flask import Blueprint
from datetime import timedelta
import arrow
import requests
import json


views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/weather", methods=["GET", "POST"])
def get_weather():
    with open("key.txt", mode="r") as file:
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
    with open("data.json", mode="w", encoding="utf-8") as file:
        json.dump(json_data, file)
    return {'success': True}
