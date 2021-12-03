import json


with open("data.json", "r", encoding="UTF-8") as file:
    dates = json.loads(file.read())['dates']
with open("results1.json", "r", encoding="UTF-8") as file:
    results = json.loads(file.read())
new_results = {}
for i in range(len(dates)):
    new_results[dates[i]] = results[i]
with open("results1.json", "w", encoding="UTF-8") as file:
    json.dump(new_results, file, ensure_ascii=False, indent=4)
