import json

quest = None
with open("src/quest.json", encoding="utf-8") as f:
    quest = json.load(f)
print(quest["quest_name"])
