import os.path
import time

import requests
import json

session = requests.session()

if os.path.exists("pics_top_50.txt"):  # makeshift cache
    with open("pics_top_50.txt", "r") as f:
        content = json.load(f)

else:
    response = session.get("https://ch.tetr.io/api/users/lists/league", params={"country": "AR"})

    if not response:
        raise ConnectionError(f"TETRIO api Error. Status code: {response.status_code}")

    content = response.json()
    with open("pics_top_50.txt", "w") as f:
        json.dump(content, f)

players = content["data"]["users"]
userids = {}
for player in players:
    userids[player["username"]] = player["_id"]

if not os.path.exists("pics_top_50/"):
    os.mkdir("pics_top_50")

for count, (username, userid) in enumerate(userids.items()):
    print(f"{count + 1}/50 downloading picture from: {username}")
    response = session.get(f"https://tetr.io/user-content/avatars/{userid}.jpg")
    with open(f"pics_top_50/{username}.jpg", "wb") as f:
        f.write(response.content)
    time.sleep(1)  # rate limiting
