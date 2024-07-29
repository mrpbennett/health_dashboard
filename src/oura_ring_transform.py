import json
import logging

import psycopg2

db = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123qwe!!",
    host="192.168.6.1",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# https://api.ouraring.com/v2/usercollection/daily_activity

# TABLE - daily_activity


def get_daily_activity(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "class_5_min": row["class_5_min"],
            "score": row["score"],
            "active_calories": row["active_calories"],
            "average_met_minutes": row["average_met_minutes"],
            "equivalent_walking_distance": row["equivalent_walking_distance"],
            "high_activity_met_minutes": row["high_activity_met_minutes"],
            "high_activity_time": row["high_activity_time"],
            "inactivity_alerts": row["inactivity_alerts"],
            "low_activity_met_minutes": row["low_activity_met_minutes"],
            "low_activity_time": row["low_activity_time"],
            "medium_activity_met_minutes": row["medium_activity_met_minutes"],
            "medium_activity_time": row["medium_activity_time"],
            "meters_to_target": row["meters_to_target"],
            "non_wear_time": row["non_wear_time"],
            "resting_time": row["resting_time"],
            "sedentary_met_minutes": row["sedentary_met_minutes"],
            "sedentary_time": row["sedentary_time"],
            "steps": row["steps"],
            "target_calories": row["target_calories"],
            "target_meters": row["target_meters"],
            "total_calories": row["total_calories"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO oura_ring.daily_activity
                            (id, day, class_5_min, score, active_calories, average_met_minutes, equivalent_walking_distance,high_activity_met_minutes,high_activity_time,inactivity_alerts,low_activity_met_minutes,low_activity_time,medium_activity_met_minutes,medium_activity_time,meters_to_target,non_wear_time,resting_time,sedentary_met_minutes,sedentary_time,steps,target_calories,target_meters,total_calories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["class_5_min"],
                            row_data["score"],
                            row_data["active_calories"],
                            row_data["average_met_minutes"],
                            row_data["equivalent_walking_distance"],
                            row_data["high_activity_met_minutes"],
                            round(row_data["high_activity_time"] / 3600, 2),
                            row_data["inactivity_alerts"],
                            row_data["low_activity_met_minutes"],
                            round(row_data["low_activity_time"] / 3600, 2),
                            row_data["medium_activity_met_minutes"],
                            round(row_data["medium_activity_time"] / 3600, 2),
                            row_data["meters_to_target"],
                            round(row_data["non_wear_time"] / 3600, 2),
                            round(row_data["resting_time"] / 3600, 2),
                            row_data["sedentary_met_minutes"],
                            round(row_data["sedentary_time"] / 3600, 2),
                            row_data["steps"],
                            row_data["target_calories"],
                            row_data["target_meters"],
                            row_data["total_calories"],
                        ),
                    )

                return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# TABLE - oura_ring.daily_activity_contributors
def get_daily_activity_contributors(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "contributors": {
                "meet_daily_targets": row["contributors"]["meet_daily_targets"],
                "move_every_hour": row["contributors"]["move_every_hour"],
                "recovery_time": row["contributors"]["recovery_time"],
                "stay_active": row["contributors"]["stay_active"],
                "training_frequency": row["contributors"]["training_frequency"],
                "training_volume": row["contributors"]["training_volume"],
            },
        }
        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                        INSERT INTO oura_ring.daily_activity_contributors
                        (id, day, meet_daily_targets, move_every_hour,recovery_time,stay_active,training_frequency,training_volume) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)
                        """,
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["contributors"]["meet_daily_targets"],
                            row_data["contributors"]["move_every_hour"],
                            row_data["contributors"]["recovery_time"],
                            row_data["contributors"]["stay_active"],
                            row_data["contributors"]["training_frequency"],
                            row_data["contributors"]["training_volume"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# https://cloud.ouraring.com/v2/usercollection/daily_sleep

# TABLE - sleep_score


def get_sleep_score(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "score": row["score"],
        }
        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                        INSERT INTO oura_ring.sleep_score
                        (id, day, score) VALUES (%s, %s, %s)
                        """,
                        (row_data["id"], row_data["day"], row_data["score"]),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# https://api.ouraring.com/v2/usercollection/sleep


# TABLE  - oura_ring.sleep
def get_sleep(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "average_breath": row["average_breath"],
            "average_heart_rate": row["average_heart_rate"],
            "average_hrv": row["average_hrv"],
            "awake_time": row["awake_time"],
            "bedtime_end": row["bedtime_end"],
            "bedtime_start": row["bedtime_start"],
            "deep_sleep_duration": row["deep_sleep_duration"],
            "efficiency": row["efficiency"],
            "latency": row["latency"],
            "light_sleep_duration": row["light_sleep_duration"],
            "lowest_heart_rate": row["lowest_heart_rate"],
            "movement_30_sec": row["movement_30_sec"],
            "period": row["period"],
            "rem_sleep_duration": row["rem_sleep_duration"],
            "restless_periods": row["restless_periods"],
            "sleep_phase_5_min": row["sleep_phase_5_min"],
            "sleep_score_delta": row["sleep_score_delta"],
            "time_in_bed": row["time_in_bed"],
            "total_sleep_duration": row["total_sleep_duration"],
            "type": row["type"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO oura_ring.sleep 
                            (id, day, average_breath,average_heart_rate,average_hrv,awake_time,bedtime_end,bedtime_start,deep_sleep_duration,efficiency,latency,light_sleep_duration,lowest_heart_rate,movement_30_sec,period,rem_sleep_duration,restless_periods,sleep_phase_5_min,sleep_score_delta,time_in_bed,total_sleep_duration,type) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """,
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["average_breath"],
                            row_data["average_heart_rate"],
                            row_data["average_hrv"],
                            round(row_data["awake_time"] / 3600, 2),
                            row_data["bedtime_end"],
                            row_data["bedtime_start"],
                            round(row_data["deep_sleep_duration"] / 3600, 2),
                            round(row_data["efficiency"] / 3600, 2),
                            round(row_data["latency"] / 3600, 2),
                            round(row_data["light_sleep_duration"] / 3600, 2),
                            row_data["lowest_heart_rate"],
                            row_data["movement_30_sec"],
                            row_data["period"],
                            round(row_data["rem_sleep_duration"] / 3600, 2),
                            round(row_data["restless_periods"] / 3600, 2),
                            row_data["sleep_phase_5_min"],
                            row_data["sleep_score_delta"],
                            round(row_data["time_in_bed"] / 3600, 2),
                            round(row_data["total_sleep_duration"] / 3600, 2),
                            row_data["type"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# TABLE - readiness
def get_readiness(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "readiness": {
                "contributors": {
                    "activity_balance": row["readiness"]["contributors"][
                        "activity_balance"
                    ],
                    "body_temperature": row["readiness"]["contributors"][
                        "body_temperature"
                    ],
                    "hrv_balance": row["readiness"]["contributors"]["hrv_balance"],
                    "previous_day_activity": row["readiness"]["contributors"][
                        "previous_day_activity"
                    ],
                    "previous_night": row["readiness"]["contributors"][
                        "previous_night"
                    ],
                    "recovery_index": row["readiness"]["contributors"][
                        "recovery_index"
                    ],
                    "resting_heart_rate": row["readiness"]["contributors"][
                        "resting_heart_rate"
                    ],
                    "sleep_balance": row["readiness"]["contributors"]["sleep_balance"],
                },
                "score": row["readiness"]["score"],
            },
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO oura_ring.readiness
                            (id, day, activity_balance, body_temperature, hrv_balance, previous_day_activity, previous_night, recovery_index, resting_heart_rate, sleep_balance, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["readiness"]["contributors"]["activity_balance"],
                            row_data["readiness"]["contributors"]["body_temperature"],
                            row_data["readiness"]["contributors"]["hrv_balance"],
                            row_data["readiness"]["contributors"][
                                "previous_day_activity"
                            ],
                            row_data["readiness"]["contributors"]["previous_night"],
                            row_data["readiness"]["contributors"]["recovery_index"],
                            row_data["readiness"]["contributors"]["resting_heart_rate"],
                            row_data["readiness"]["contributors"]["sleep_balance"],
                            row_data["readiness"]["score"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# https://cloud.ouraring.com/v2/usercollection/sleep_time


# TABLE - sleep_time
def get_sleep_time(data) -> bool:

    table_error = json.loads(data)

    for row in table_error["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "optimal_bedtime": {
                "end_offset": row["optimal_bedtime"]["end_offset"],
                "start_offset": row["optimal_bedtime"]["start_offset"],
            },
            "recommendation": row["recommendation"],
            "status": row["status"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        "INSERT INTO oura_ring.sleep_time (id, day, end_offset, start_offset, recommendation, status) VALUES (%s, %s,%s, %s, %s, %s)",
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["optimal_bedtime"]["end_offset"],
                            row_data["optimal_bedtime"]["start_offset"],
                            row_data["recommendation"],
                            row_data["status"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# https://api.ouraring.com/v2/usercollection/daily_stress


# TABLE - daily_stress
def get_stress(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "stress_high": row["stress_high"],
            "recovery_high": row["recovery_high"],
            "day_summary": row["day_summary"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO oura_ring.stress
                            (id, day, stress_high, recovery_high, day_summary) VALUES (%s, %s, %s, %s, %s)""",
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["stress_high"],
                            row_data["recovery_high"],
                            row_data["day_summary"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# https://api.ouraring.com/v2/usercollection/daily_spo2


# TABLE - blood_oxygen
def get_blood_oxygen(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "spo2_percentage": {
                "average": row["spo2_percentage"]["average"],
            },
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO oura_ring.blood_oxygen
                            (id, day, spo2_percentage) VALUES (%s, %s, %s)""",
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["spo2_percentage"]["average"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False


# https://cloud.ouraring.com/v2/usercollection/workout


# TABLE - workout
def get_workout(data) -> bool:

    table_data = json.loads(data)

    for row in table_data["data"]:

        row_data = {
            "id": row["id"],
            "day": row["day"],
            "activity": row["activity"],
            "calories": row["calories"],
            "distance": row["distance"],
            "end_datetime": row["end_datetime"],
            "intensity": row["intensity"],
            "label": row["label"],
            "source": row["source"],
            "start_datetime": row["start_datetime"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                        INSERT INTO oura_ring.workout(id, day, activity, calories, distance, end_datetime, intensity, label, source , start_datetime)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s),
                        """,
                        (
                            row_data["id"],
                            row_data["day"],
                            row_data["activity"],
                            row_data["calories"],
                            row_data["distance"],
                            row_data["end_datetime"],
                            row_data["intensity"],
                            row_data["label"],
                            row_data["source"],
                            row_data["start_datetime"],
                        ),
                    )
            return True

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    return False
