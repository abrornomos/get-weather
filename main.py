import json


with open("results.json", "r", encoding="UTF-8") as file:
    results = json.loads(file.read())
new_results = {}
for key, value in results:
    hours = value['hours']
    temp = {
        'airTemperature': {
            'noaa': 0,
            'sg': 0
        },
        'cloudCover': {
            'noaa': 0,
            'sg': 0
        },
        'currentDirection': {
            'meto': 0,
            'sg': 0
        },
        'currentSpeed': {
            'meto': 0,
            'sg': 0
        },
        'gust': {
            'noaa': 0,
            'sg': 0
        },
        'humidity': {
            'noaa': 0,
            'sg': 0
        },
        'precipitation': {
            'noaa': 0,
            'sg': 0
        },
        'pressure': {
            'noaa': 0,
            'sg': 0
        },
        'windDirection': {
            'icon': 0,
            'noaa': 0,
            'sg': 0
        },
        'windSpeed': {
            'icon': 0,
            'noaa': 0,
            'sg': 0
        }
    }
    for values in hours:
        for hours_key, hours_value in values:
            if hours_key != 'time':
                for 
with open("averageResults.json", "w", encoding="UTF-8") as file:
    json.dump(new_results, file, ensure_ascii=False, indent=4)
