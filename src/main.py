import json
import logging
import os
from datetime import date, timedelta

import garminconnect
import tomli

from garmin_transform import (
    insert_garmin_readiness,
    insert_garmin_sleep,
    insert_garmin_sleep_body_battery,
    insert_garmin_sleep_heart_rate,
    insert_garmin_sleep_hrv,
    insert_garmin_stats,
)
from oura_ring_extract import (
    get_usercollection_daily_activity,
    get_usercollection_daily_sleep,
    get_usercollection_daily_spo2,
    get_usercollection_sleep,
    get_usercollection_sleep_time,
    get_usercollection_stress,
    get_usercollection_workout,
)
from oura_ring_transform import (
    get_blood_oxygen,
    get_daily_activity,
    get_daily_activity_contributors,
    get_readiness,
    get_sleep,
    get_sleep_score,
    get_sleep_time,
    get_stress,
    get_workout,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# --- CONFIG ---
# PROD
with open("/app/src/config.toml", mode="rb") as config_file:
    config = tomli.load(config_file)

# DEV
# with open("./config.toml", mode="rb") as config_file:
#     config = tomli.load(config_file)


# YESTERDAY
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.isoformat()


# GARMIN
garmin = garminconnect.Garmin(config["garmin"]["email"], config["garmin"]["password"])
garmin.login()
garmin.display_name

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)

# GARMIN DATA
get_stats_and_body = garmin.get_stats_and_body(yesterday)
get_sleep_data = garmin.get_sleep_data(yesterday)
get_garmin_readiness = garmin.get_training_readiness(yesterday)


# OURA RING
daily_activity = get_usercollection_daily_activity()
daily_sleep = get_usercollection_daily_sleep()
sleep = get_usercollection_sleep()
sleep_time = get_usercollection_sleep_time()
stress = get_usercollection_stress()
blood_o2 = get_usercollection_daily_spo2()
workout = get_usercollection_workout()


def main():

    # GARMIN
    # SLEEP -------------------------------------------
    # TABLE - garmin.sleep
    if insert_garmin_sleep(get_sleep_data):
        logging.info("garmin.sleep has been updated")
    # TABLE - garmin.sleep_hrv
    if insert_garmin_sleep_hrv(get_sleep_data):
        logging.info("garmin_sleep_hrv has been updated")
    # TABLE - garmin.sleep_heart_rate
    if insert_garmin_sleep_heart_rate(get_sleep_data):
        logging.info("garmin.sleep_heart_rate has been updated")
    # TABLE - garmin.sleep_body_battery
    if insert_garmin_sleep_body_battery(get_sleep_data):
        logging.info("garmin.sleep_body_battery has been updated")

    # STATS -------------------------------------------
    # TABLE - garmin.stats
    if insert_garmin_stats(get_stats_and_body):
        logging.info("garmin.stats has been updated")

    # READINESS -------------------------------------------
    # TABLE - garmin.readiness
    if insert_garmin_readiness(get_garmin_readiness):
        logging.info("garmin.readiness has been updated")

    # OURA RING

    # https://api.ouraring.com/v2/usercollection/daily_activity
    # TABLE - daily_activity
    if get_daily_activity(daily_activity):
        logging.info("daily_activity table has been updated")

    # TABLE - daily_activity_contributors
    if get_daily_activity_contributors(daily_activity):
        logging.info("daily_activity_contributors table has been updated")

    # https://cloud.ouraring.com/v2/usercollection/daily_sleep
    # TABLE - sleep_score
    if get_sleep_score(daily_sleep):
        logging.info("sleep_score table has been updated")

    # https://api.ouraring.com/v2/usercollection/sleep
    # TABLE - sleep
    if get_sleep(sleep):
        logging.info("sleep table has been updated")

    # TABLE - readiness
    if get_readiness(sleep):
        logging.info("readiness table has been updated")

    # https://cloud.ouraring.com/v2/usercollection/sleep_time
    # TABLE - sleep_time
    if get_sleep_time(sleep_time):
        logging.info("sleep_time table has been updated")

    # https://api.ouraring.com/v2/usercollection/daily_stress
    # TABLE - stress
    if get_stress(stress):
        logging.info("stress table has been updated")

    # https://api.ouraring.com/v2/usercollection/daily_spo2
    # TABLE - blood_oxygen
    if get_blood_oxygen(blood_o2):
        logging.info("blood_oxygen table has been updated")

    # https://cloud.ouraring.com/v2/usercollection/workout
    # TABLE - workout
    if get_workout(workout):
        logging.info("workout table has been updated")


if __name__ == "__main__":
    main()
