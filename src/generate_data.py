import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# =========================
# CONFIG
# =========================
np.random.seed(42)
random.seed(42)

N_USERS = 50000
BASE_DATE = datetime(2026, 1, 1)

CITIES = [
    "Jakarta",
    "Surabaya",
    "Bandung",
    "Yogyakarta",
    "Medan"
]

CITY_PROBS = [0.35, 0.20, 0.20, 0.15, 0.10]

DEVICES = ["Android", "iOS"]
DEVICE_PROBS = [0.75, 0.25]

SEGMENTS = ["New", "Returning", "Power"]
SEGMENT_PROBS = [0.40, 0.45, 0.15]


# =========================
# HELPER FUNCTIONS
# =========================
def is_peak_hour(session_time):
    hour = session_time.hour

    morning_peak = 7 <= hour <= 9
    evening_peak = 17 <= hour <= 20

    return morning_peak or evening_peak


def generate_eta(city):
    city_eta = {
        "Jakarta": 10,
        "Surabaya": 6,
        "Bandung": 7,
        "Yogyakarta": 5,
        "Medan": 8
    }

    mean_eta = city_eta[city]

    eta = np.random.normal(mean_eta, 2)

    return max(2, round(eta))


def generate_surge(is_peak):
    if is_peak:
        surge = np.random.uniform(1.2, 2.5)
    else:
        surge = np.random.uniform(1.0, 1.3)

    return round(surge, 2)


def generate_fare(city, surge_multiplier):
    base_fare = {
        "Jakarta": 18000,
        "Surabaya": 14000,
        "Bandung": 15000,
        "Yogyakarta": 12000,
        "Medan": 13000
    }

    fare = base_fare[city] * surge_multiplier
    noise = np.random.uniform(0.9, 1.1)

    fare *= noise

    return round(fare)


# =========================
# DATA GENERATION
# =========================
def generate_users():
    users = []

    for i in range(1, N_USERS + 1):
        user_id = f"U{i:06d}"

        signup_offset = np.random.randint(0, 730)
        signup_date = (
            BASE_DATE - timedelta(days=int(signup_offset))
        ).date()

        city = np.random.choice(
            CITIES,
            p=CITY_PROBS
        )

        device_type = np.random.choice(
            DEVICES,
            p=DEVICE_PROBS
        )

        user_segment = np.random.choice(
            SEGMENTS,
            p=SEGMENT_PROBS
        )

        if user_segment == "New":
            total_completed_rides = np.random.randint(0, 6)

        elif user_segment == "Returning":
            total_completed_rides = np.random.randint(6, 51)

        else:  # Power
            total_completed_rides = np.random.randint(51, 301)

        users.append([
            user_id,
            signup_date,
            city,
            device_type,
            user_segment,
            total_completed_rides
        ])

    users_df = pd.DataFrame(
        users,
        columns=[
            "user_id",
            "signup_date",
            "city",
            "device_type",
            "user_segment",
            "total_completed_rides"
        ]
    )

    users_df["signup_date"] = pd.to_datetime(users_df["signup_date"])

    print(users_df.head())
    print(f"Total users generated: {len(users_df)}")

    return users_df


def generate_sessions(users_df):
    sessions = []
    session_counter = 1

    for _, user in users_df.iterrows():
        segment = user["user_segment"]

        if segment == "New":
            n_sessions = np.random.randint(1, 4)

        elif segment == "Returning":
            n_sessions = np.random.randint(4, 13)

        else:  # Power
            n_sessions = np.random.randint(15, 41)

        for _ in range(n_sessions):
            session_id = f"S{session_counter:07d}"
            session_counter += 1

            days_offset = np.random.randint(0, 90)
            minutes_offset = np.random.randint(0, 1440)

            session_start = (
                BASE_DATE
                + timedelta(
                    days=int(days_offset),
                    minutes=int(minutes_offset)
                )
            )

            peak_hour = is_peak_hour(session_start)

            eta_minutes = generate_eta(user["city"])

            surge_multiplier = generate_surge(peak_hour)

            estimated_fare = generate_fare(
                user["city"],
                surge_multiplier
            )

            sessions.append([
                session_id,
                user["user_id"],
                session_start,
                user["city"],
                user["device_type"],
                user["user_segment"],
                eta_minutes,
                surge_multiplier,
                estimated_fare,
                peak_hour
            ])

    sessions_df = pd.DataFrame(
        sessions,
        columns=[
            "session_id",
            "user_id",
            "session_start",
            "city",
            "device_type",
            "user_segment",
            "eta_minutes",
            "surge_multiplier",
            "estimated_fare",
            "is_peak_hour"
        ]
    )

    print(sessions_df.head())
    print(f"Total sessions generated: {len(sessions_df)}")

    return sessions_df


def generate_events(sessions_df):
    events = []
    event_counter = 1

    for _, session in sessions_df.iterrows():
        session_id = session["session_id"]
        user_id = session["user_id"]
        base_time = session["session_start"]

        segment = session["user_segment"]
        surge = session["surge_multiplier"]
        eta = session["eta_minutes"]

        # Base probabilities by segment
        if segment == "New":
            p_request = 0.60
            p_driver = 0.82
            p_complete = 0.92

        elif segment == "Returning":
            p_request = 0.75
            p_driver = 0.87
            p_complete = 0.95

        else:  # Power
            p_request = 0.90
            p_driver = 0.93
            p_complete = 0.98

        # Surge penalty
        if surge > 1.8:
            p_request -= 0.25
        elif surge > 1.4:
            p_request -= 0.12

        # ETA penalty
        if eta > 12:
            p_driver -= 0.15
        elif eta > 8:
            p_driver -= 0.08

        session_events = [
            "app_open",
            "destination_selected",
            "fare_shown"
        ]

        if np.random.rand() < p_request:
            session_events.append("ride_requested")

            if np.random.rand() < p_driver:
                session_events.append("driver_assigned")

                if np.random.rand() < p_complete:
                    session_events.append("ride_completed")
                else:
                    session_events.append("booking_cancelled")
            else:
                session_events.append("booking_cancelled")
        else:
            session_events.append("booking_cancelled")

        for step, event_name in enumerate(session_events):
            event_id = f"E{event_counter:08d}"
            event_counter += 1

            event_time = base_time + timedelta(seconds=step * 30)

            events.append([
                event_id,
                session_id,
                user_id,
                event_name,
                event_time
            ])

    events_df = pd.DataFrame(
        events,
        columns=[
            "event_id",
            "session_id",
            "user_id",
            "event_name",
            "event_time"
        ]
    )

    print(events_df.head())
    print(f"Total events generated: {len(events_df)}")

    return events_df


def generate_experiments(sessions_df, events_df):
    experiment_df = sessions_df.copy()

    experiment_df = experiment_df[
        experiment_df["surge_multiplier"] >= 1.3
    ].copy()

    experiment_df["experiment_id"] = [
        f"EXP{i:07d}"
        for i in range(1, len(experiment_df) + 1)
    ]

    experiment_df["variant"] = np.random.choice(
        ["Control", "Treatment"],
        size=len(experiment_df),
        p=[0.5, 0.5]
    )

    experiment_df["discount_badge_shown"] = (
        experiment_df["variant"] == "Treatment"
    )

    requested_sessions = set(
        events_df[
            events_df["event_name"] == "ride_requested"
        ]["session_id"]
    )

    experiment_df["conversion"] = (
        experiment_df["session_id"]
        .isin(requested_sessions)
        .astype(int)
    )

    experiment_df = experiment_df[
        [
            "experiment_id",
            "session_id",
            "variant",
            "discount_badge_shown",
            "conversion"
        ]
    ]

    print(experiment_df.head())
    print(
        f"Total experiment rows generated: "
        f"{len(experiment_df)}"
    )

    return experiment_df


# =========================
# SAVE CSV
# =========================
def save_dataframes(
    users_df,
    sessions_df,
    events_df,
    experiments_df
):
    os.makedirs("data/raw", exist_ok=True)

    users_df.to_csv(
        "data/raw/users.csv",
        index=False
    )

    sessions_df.to_csv(
        "data/raw/ride_sessions.csv",
        index=False
    )

    events_df.to_csv(
        "data/raw/ride_events.csv",
        index=False
    )

    experiments_df.to_csv(
        "data/raw/experiments.csv",
        index=False
    )

    print("\nAll datasets saved successfully.")


# =========================
# MAIN
# =========================
def main():
    users_df = generate_users()
    sessions_df = generate_sessions(users_df)
    events_df = generate_events(sessions_df)
    experiments_df = generate_experiments(
        sessions_df,
        events_df
    )

    save_dataframes(
        users_df,
        sessions_df,
        events_df,
        experiments_df
    )


if __name__ == "__main__":
    main()
