import logging
from datetime import datetime, timedelta

import requests
import tomli

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# PROD
with open("/app/src/config.toml", mode="rb") as config_file:
    config = tomli.load(config_file)

# DEV
# with open("./config.toml", mode="rb") as config_file:
#     config = tomli.load(config_file)

# Get today's date
today = datetime.now().date()
yesterday = today - timedelta(days=1)


def get_usercollection_daily_activity():
    url = "https://api.ouraring.com/v2/usercollection/daily_activity"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{today}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text


def get_usercollection_daily_sleep():
    url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{yesterday}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text


def get_usercollection_sleep():
    url = "https://api.ouraring.com/v2/usercollection/sleep"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{today}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text


def get_usercollection_sleep_time():
    url = "https://api.ouraring.com/v2/usercollection/sleep_time"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{today}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text


def get_usercollection_stress():
    url = "https://api.ouraring.com/v2/usercollection/daily_stress"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{yesterday}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text


def get_usercollection_daily_spo2():
    url = "https://api.ouraring.com/v2/usercollection/daily_spo2"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{yesterday}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text


def get_usercollection_workout():
    url = "https://api.ouraring.com/v2/usercollection/workout"
    headers = {"Authorization": f"Bearer {config['oura']['token']}"}
    params = {"start_date": f"{yesterday}", "end_date": f"{yesterday}"}
    response = requests.request("GET", url, headers=headers, params=params)

    return response.text
