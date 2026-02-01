# main.py
from client import StravaClient
import time
import json
from datetime import timedelta
from collections import defaultdict

client = StravaClient()
#print("Access token (auto-refreshed if needed):", client.access_token)
activities = client.get_activities(per_page=50, after=int(time.time()) - 86400 * 30)

grouped = defaultdict(list)

for activity in activities:
    grouped[activity["type"]].append(activity)

for name, activities in grouped.items():
    print(name)
    for activity in activities:
        print(activity["name"], activity["distance"], activity["moving_time"])

    #if activity["type"] == "Ride":
    #    dist_in_miles = activity["distance"] * 0.000621371
    #    moving_time = str(timedelta(seconds=activity["moving_time"]))
    #    print(activity["name"], dist_in_miles, moving_time)