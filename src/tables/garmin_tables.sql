CREATE SCHEMA IF NOT EXISTS garmin;

CREATE TABLE garmin.sleep(
    id BIGINT PRIMARY KEY,
    day DATE,
    sleep_time_hours BIGINT,
    sleep_window_confirmed BOOLEAN,
    sleep_start_time VARCHAR,
    sleep_end_time VARCHAR,
    sleep_score BIGINT,
    deep_sleep_hours FLOAT,
    deep_sleep_pct BIGINT,
    light_sleep_hours FLOAT,
    light_sleep_pct BIGINT,
    rem_sleep_hours FLOAT,
    rem_sleep_pct BIGINT,
    awake_sleep_hours FLOAT,
    average_respiration_value FLOAT,
    lowest_respiration_value FLOAT,
    highest_respiration_value FLOAT,
    avg_sleep_stress FLOAT,
    sleep_score_feedback VARCHAR(255),
    sleep_score_insight VARCHAR(255),
    avg_overnight_hrv FLOAT,
    hrv_status VARCHAR(255),
    body_battery_change BIGINT,
    resting_heart_rate BIGINT
);

CREATE TABLE garmin.sleep_hrv(
    start_gmt_epoch BIGINT,
    value FLOAT
);

CREATE TABLE garmin.sleep_body_battery(
    start_gmt_epoch BIGINT,
    value FLOAT
);

CREATE TABLE garmin.sleep_heart_rate(
    start_gmt_epoch BIGINT,
    value FLOAT
);

CREATE TABLE garmin.stats(
    id BIGINT PRIMARY KEY,
    day DATE,
    total_calories BIGINT,
    active_calories INT,
    bmr_calories INT,
    total_steps INT,
    highly_active_hours FLOAT,
    active_hours FLOAT,
    sedentary_hours FLOAT,
    sleep_hours FLOAT,
    min_heart_rate INT,
    max_heart_rate INT,
    resting_heart_rate INT,
    avg_stress_level INT,
    max_stress_level INT,
    stress_percentage FLOAT,
    rest_stress_percentage FLOAT,
    low_stress_percentage FLOAT,
    activity_stress_percentage FLOAT,
    uncategorized_stress_percentage FLOAT,
    medium_stress_percentage FLOAT,
    high_stress_percentage FLOAT,
    bodybattery_charged_value INT,
    bodybattery_drained_value INT,
    bodybattery_highest_value INT,
    bodybattery_lowest_value INT,
    bodybattery_most_recent_value INT,
    bodybattery_during_sleep INT,
    avg_waking_respiration_value FLOAT,
    highest_respiration_value FLOAT,
    lowest_respiration_value FLOAT,
    latest_respiration_value FLOAT,
    body_weight FLOAT,
    bmi FLOAT,
    body_fat FLOAT,
    body_water FLOAT,
    bone_mass FLOAT,
    muscle_mass FLOAT,
    physique_rating VARCHAR(255),
    visceral_fat FLOAT,
    metabolic_age INT
);