import csv
from datetime import datetime, timedelta
import random

header = ["Date", "App_Name", "Category", "Minutes_Used"]

apps = [
    ("Instagram", "Social Media"),
    ("YouTube", "Entertainment"),
    ("VS Code", "Coding"),
    ("LeetCode", "Education"),
    ("Spotify", "Entertainment"),
    ("WhatsApp", "Communication"),
    ("Chrome", "Productivity")
]

minutes_range = {
    "Instagram": (60, 150),
    "YouTube": (40, 120),
    "VS Code": (120, 240),
    "LeetCode": (30, 90),
    "Spotify": (20, 60),
    "WhatsApp": (30, 90),
    "Chrome": (40, 100),
}

rows = []

start_date = datetime(2026, 7, 20)

for i in range(14):  # 14 days
    current_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

    for app, category in apps:
       low, high = minutes_range[app]
       minutes = random.randint(low, high)
       rows.append([current_date, app, category, minutes])

        
with open("screentime.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

print("screentime.csv created successfully!")
