import os
from datetime import date, timedelta

import garminconnect

from garmin_transform import insert_garmin_sleep

email = "pbennett.uk@gmail.com"
password = "U5BX#w4Adp7q"

garmin = garminconnect.Garmin(email, password)
garmin.login()

garmin.display_name

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)

yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.isoformat()

get_stats = garmin.get_stats(yesterday)
get_user_summary = garmin.get_user_summary(yesterday)
get_body_battery = garmin.get_body_battery(yesterday)
get_respiration_data = garmin.get_respiration_data(yesterday)
get_stats_and_body = garmin.get_stats_and_body(yesterday)
# get_activities = garmin.get_activities(yesterday, 1)
get_sleep_data = garmin.get_sleep_data(yesterday)


# INSERT GARMIN SLEEP DATA
def get_garmin_sleep_data():
    return [insert_garmin_sleep(get_sleep_data)]


# with open("get_stats.json", "w") as f:
#     f.write(json.dumps(get_stats, indent=2))

# with open("get_user_summary.json", "w") as f:
#     f.write(json.dumps(get_user_summary, indent=2))

# with open("get_body_battery.json", "w") as f:
#     f.write(json.dumps(get_body_battery, indent=2))

# with open("get_respiration_data.json", "w") as f:
#     f.write(json.dumps(get_respiration_data, indent=2))

# with open("get_stats_and_body.json", "w") as f:
#     f.write(json.dumps(get_stats_and_body, indent=2))

# # with open("get_activities.json", "w") as f:
# #     f.write(json.dumps(get_activities, indent=2))

# with open("get_sleep_data.json", "w") as f:
#     f.write(json.dumps(get_sleep_data, indent=2))


# print(heart_rate)
