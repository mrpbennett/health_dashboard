CREATE TABLE oura_ring.sleep_hrv (
    id SERIAL PRIMARY KEY,
    value DECIMAL,
    timestamp TIMESTAMPTZ
);

CREATE TABLE oura_ring.sleep_heart_rate (
    id SERIAL PRIMARY KEY,
    value DECIMAL,
    timestamp TIMESTAMPTZ
);

CREATE TABLE oura_ring.sleep_daily (
    id VARCHAR PRIMARY KEY,
    awake_time INT,
    deep_sleep_duration INT,
    efficiency INT,
    latency INT,
    light_sleep_duration INT,
    rem_sleep_duration INT,
    restless_periods INT,
    time_in_bed INT,
    total_sleep_duration INT,
    type VARCHAR,
    day DATE
);

CREATE TABLE oura_ring.sleep_readiness (
    id VARCHAR PRIMARY KEY,
    activity_balance INT,
    body_temperature INT,
    hrv_balance INT,
    previous_day_activity INT,
    previous_night INT,
    recovery_index INT,
    resting_heart_rate INT,
    sleep_balance INT,
    score INT,
    day DATE
);

CREATE TABLE oura_ring.daily_stress (
    id VARCHAR PRIMARY KEY,
    stress_high INT,
    recovery_high INT,
    day_summary VARCHAR,
    day DATE
);

CREATE TABLE oura_ring.daily_blood_oxygen (
    id VARCHAR PRIMARY KEY,
    spo2_percentage INT,
    day DATE
);

CREATE TABLE oura_ring.daily_activity (
    id VARCHAR PRIMARY KEY,
    score INT,
    active_calories INT,
    target_calories INT,
    total_calories INT,
    resting_time INT,
    sedentary_time INT,
    steps INT,
    day DATE
);

-- GRAFANA
CREATE USER grafanareader WITH PASSWORD 'password';

GRANT USAGE ON SCHEMA oura_ring TO grafanareader;

GRANT
SELECT
    ON oura_ring.sleep_daily TO grafanareader;

GRANT
SELECT
    ON oura_ring.sleep_hrv TO grafanareader;

GRANT
SELECT
    ON oura_ring.sleep_heart_rate TO grafanareader;

GRANT
SELECT
    ON oura_ring.daily_activity TO grafanareader;

GRANT
SELECT
    ON oura_ring.daily_blood_oxygen TO grafanareader;

GRANT
SELECT
    ON oura_ring.daily_stress TO grafanareader;

GRANT
SELECT
    ON oura_ring.sleep_readiness TO grafanareader;

ALTER ROLE grafanareader
SET
    search_path = oura_ring;