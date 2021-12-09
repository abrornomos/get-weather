from arrow import Arrow
from flask import Blueprint, render_template
import json
import requests


views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/weather", methods=["GET", "POST"])
def weather():
    with open("database/data.json", "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
    dates = data['dates']
    with open("database/key.txt", "r") as file:
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
            data['stormglass_api'],
            params={
                'lat': data['latitude'],
                'lng': data['longitude'],
                'params': ",".join(keys),
                'start': start.to('UTC').timestamp(),
                'end': end.to('UTC').timestamp()
            },
            headers={
                'Authorization': data['stormglass_api_tokens'][token_index]
            }
        )
        json_data[date['date']] = response.json()
    results = {}
    for date in json_data:
        hours = json_data[date]['hours']
        if isinstance(hours, list):
            temp = {}
            for hour in hours:
                for param in hour:
                    if param != 'time':
                        if param not in temp:
                            temp[param] = {}
                        for key in hour[param]:
                            if key in temp[param]:
                                temp[param][key] += hour[param][key]
                            else:
                                temp[param][key] = hour[param][key]
            for param in temp:
                for key in temp[param]:
                    temp[param][key] = round(temp[param][key] / len(hours), 3)
            results[date] = {
                'hours': temp,
                'meta': json_data[date]['meta']
            }
        else:
            results[date] = json_data[date]
    with open("database/results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    return results
