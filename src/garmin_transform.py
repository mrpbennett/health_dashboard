import datetime
import json
import logging

import psycopg2

db = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="password",
    host="192.168.5.52",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)


def get_column_count(conn, schema_name, table_name):
    with conn.cursor() as curs:
        curs.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            """,
            (schema_name, table_name),
        )
        count = curs.fetchone()[0]
    return count


def insert_garmin_sleep(data) -> bool:

    with open("data.json", "w") as f:
        f.write(json.dumps(data, indent=4))

    row_data = {
        "id": data["dailySleepDTO"]["id"],
        "day": data["dailySleepDTO"]["calendarDate"],
        "sleep_time_hours": round(data["dailySleepDTO"]["sleepTimeSeconds"] / 3200, 2),
        "sleep_window_confirmed": data["dailySleepDTO"]["sleepWindowConfirmed"],
        "sleep_start_time": datetime.datetime.fromtimestamp(
            data["dailySleepDTO"]["sleepStartTimestampGMT"] / 1000
        ).strftime("%H:%M"),
        "sleep_end_time": datetime.datetime.fromtimestamp(
            data["dailySleepDTO"]["sleepEndTimestampGMT"] / 1000
        ).strftime("%H:%M"),
        "sleep_score": data["dailySleepDTO"]["sleepScores"]["overall"]["value"],
        "deep_sleep_hours": round(data["dailySleepDTO"]["deepSleepSeconds"] / 3200, 2),
        "deep_sleep_pct": data["dailySleepDTO"]["sleepScores"]["deepPercentage"][
            "value"
        ],
        "light_sleep_hours": round(
            data["dailySleepDTO"]["lightSleepSeconds"] / 3200, 2
        ),
        "light_sleep_pct": data["dailySleepDTO"]["sleepScores"]["lightPercentage"][
            "value"
        ],
        "rem_sleep_hours": round(data["dailySleepDTO"]["remSleepSeconds"] / 3200, 2),
        "rem_sleep_pct": data["dailySleepDTO"]["sleepScores"]["remPercentage"]["value"],
        "awake_sleep_hours": round(
            data["dailySleepDTO"]["awakeSleepSeconds"] / 3200, 2
        ),
        "average_respiration_value": data["dailySleepDTO"]["averageRespirationValue"],
        "lowest_respiration_value": data["dailySleepDTO"]["lowestRespirationValue"],
        "highest_respiration_value": data["dailySleepDTO"]["highestRespirationValue"],
        "avg_sleep_stress": data["dailySleepDTO"]["avgSleepStress"],
        "sleep_score_feedback": data["dailySleepDTO"]["sleepScoreFeedback"],
        "sleep_score_insight": data["dailySleepDTO"]["sleepScoreInsight"],
        "avg_overnight_hrv": data["avgOvernightHrv"],
        "hrv_status": data["hrvStatus"],
        "body_battery_change": data["bodyBatteryChange"],
        "resting_heart_rate": data["restingHeartRate"],
    }

    columns = [
        "id",
        "day",
        "sleep_time_hours",
        "sleep_window_confirmed",
        "sleep_start_time",
        "sleep_end_time",
        "sleep_score",
        "deep_sleep_hours",
        "deep_sleep_pct",
        "light_sleep_hours",
        "light_sleep_pct",
        "rem_sleep_hours",
        "rem_sleep_pct",
        "awake_sleep_hours",
        "average_respiration_value",
        "lowest_respiration_value",
        "highest_respiration_value",
        "avg_sleep_stress",
        "sleep_score_feedback",
        "sleep_score_insight",
        "avg_overnight_hrv",
        "hrv_status",
        "body_battery_change",
        "resting_heart_rate",
    ]

    values = [row_data[col] for col in columns]

    try:
        with db as conn:

            column_count = get_column_count(conn, "garmin", "sleep")
            logging.info(f"Column count in garmin.sleep: {column_count}")

            if len(values) != column_count:
                logging.error(
                    f"Mismatch between number of columns ({column_count}) and values ({len(values)})"
                )
                return False

            with conn.cursor() as curs:
                curs.execute(
                    f"""
                        INSERT INTO garmin.sleep ({', '.join(columns)}) 
                        VALUES ({', '.join(['%s'] * len(values))})
                    """,
                    tuple(values),
                )

        return True

    except KeyError as ke:
        logging.error(f"Missing key in data: {ke}")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")

    return False


def insert_garmin_sleep_hrv(data) -> bool:

    hrv_data = data["hrvData"]

    for row in hrv_data:

        row_data = {
            "start_gmt_epoch": row["startGMT"],
            "value": row["value"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO garmin.sleep_hrv
                            (start_gmt_epoch, value) VALUES (%s,%s)
                            """,
                        (row_data["start_gmt_epoch"], row_data["value"]),
                    )
        except Exception as e:
            logging.error(e)

    return True


def insert_garmin_sleep_heart_rate(data) -> bool:

    hrv_data = data["sleepHeartRate"]

    for row in hrv_data:

        row_data = {
            "start_gmt_epoch": row["startGMT"],
            "value": row["value"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO garmin.sleep_heart_rate
                            (start_gmt_epoch, value) VALUES (%s,%s)
                            """,
                        (row_data["start_gmt_epoch"], row_data["value"]),
                    )

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

            return True

    return False


def insert_garmin_sleep_body_battery(data) -> bool:

    hrv_data = data["sleepBodyBattery"]

    for row in hrv_data:

        row_data = {
            "start_gmt_epoch": row["startGMT"],
            "value": row["value"],
        }

        try:
            with db as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                            INSERT INTO garmin.sleep_body_battery
                            (start_gmt_epoch, value) VALUES (%s,%s)
                            """,
                        (row_data["start_gmt_epoch"], row_data["value"]),
                    )

        except KeyError as ke:
            logging.error(f"Missing key in data: {ke}")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

            return True

    return False


def insert_garmin_stats(data) -> bool:

    try:

        row_data = {
            "id": data["userDailySummaryId"],
            "day": data["calendarDate"],
            "total_calories": data["totalKilocalories"],
            "active_calories": data["activeKilocalories"],
            "bmr_calories": data["bmrKilocalories"],
            "total_steps": data["totalSteps"],
            "highly_active_hours": round(data["highlyActiveSeconds"] / 3200, 2),
            "active_hours": round(data["activeSeconds"] / 3200, 2),
            "sedentary_hours": round(data["sedentarySeconds"] / 3200, 2),
            "sleep_hours": round(data["sleepingSeconds"] / 3200, 2),
            "min_heart_rate": data["minHeartRate"],
            "max_heart_rate": data["maxHeartRate"],
            "resting_heart_rate": data["restingHeartRate"],
            "avg_stress_level": data["averageStressLevel"],
            "max_stress_level": data["maxStressLevel"],
            "stress_percentage": data["stressPercentage"],
            "rest_stress_percentage": data["restStressPercentage"],
            "low_stress_percentage": data["lowStressPercentage"],
            "activity_stress_percentage": data["activityStressPercentage"],
            "uncategorized_stress_percentage": data["uncategorizedStressPercentage"],
            "medium_stress_percentage": data["mediumStressPercentage"],
            "high_stress_percentage": data["highStressPercentage"],
            "min_heart_rate": data["minHeartRate"],
            "max_heart_rate": data["maxHeartRate"],
            "bodybattery_charged_value": data["bodyBatteryChargedValue"],
            "bodybattery_drained_value": data["bodyBatteryDrainedValue"],
            "bodybattery_highest_value": data["bodyBatteryHighestValue"],
            "bodybattery_lowest_value": data["bodyBatteryLowestValue"],
            "bodybattery_most_recent_value": data["bodyBatteryMostRecentValue"],
            "bodybattery_during_sleep": data["bodyBatteryDuringSleep"],
            "avg_waking_respiration_value": data["avgWakingRespirationValue"],
            "highest_respiration_value": data["highestRespirationValue"],
            "lowest_respiration_value": data["lowestRespirationValue"],
            "latest_respiration_value": data["latestRespirationValue"],
            "body_weight": data["weight"],
            "bmi": data["bmi"],
            "body_fat": data["bodyFat"],
            "body_water": data["bodyWater"],
            "bone_mass": data["boneMass"],
            "muscle_mass": data["muscleMass"],
            "physique_rating": data["physiqueRating"],
            "visceral_fat": data["visceralFat"],
            "metabolic_age": data["physiqueRating"],
        }

        columns = [
            "id",
            "day",
            "total_calories",
            "active_calories",
            "bmr_calories",
            "total_steps",
            "highly_active_hours",
            "active_hours",
            "sedentary_hours",
            "sleep_hours",
            "min_heart_rate",
            "max_heart_rate",
            "resting_heart_rate",
            "avg_stress_level",
            "max_stress_level",
            "stress_percentage",
            "rest_stress_percentage",
            "low_stress_percentage",
            "activity_stress_percentage",
            "uncategorized_stress_percentage",
            "medium_stress_percentage",
            "high_stress_percentage",
            "bodybattery_charged_value",
            "bodybattery_drained_value",
            "bodybattery_highest_value",
            "bodybattery_lowest_value",
            "bodybattery_most_recent_value",
            "bodybattery_during_sleep",
            "avg_waking_respiration_value",
            "highest_respiration_value",
            "lowest_respiration_value",
            "latest_respiration_value",
            "body_weight",
            "bmi",
            "body_fat",
            "body_water",
            "bone_mass",
            "muscle_mass",
            "physique_rating",
            "visceral_fat",
            "metabolic_age",
        ]

        values = [row_data[col] for col in columns]

        logging.info(f"Number of columns: {len(columns)}")
        logging.info(f"Number of values: {len(values)}")

        with db as conn:
            column_count = get_column_count(conn, "garmin", "stats")
            logging.info(f"Column count in database: {column_count}")

            if len(values) != column_count:
                logging.error(
                    f"Mismatch between number of columns ({column_count}) and values ({len(values)})"
                )
                return False

            with conn.cursor() as curs:
                curs.execute(
                    f"""
                        INSERT INTO garmin.stats ({', '.join(columns)}) 
                        VALUES ({', '.join(['%s'] * len(values))})
                    """,
                    tuple(values),
                )
        return True

    except KeyError as ke:
        logging.error(f"Missing key in data: {ke}")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")

    return False
