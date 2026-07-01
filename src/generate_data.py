# imports
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# config
np.random.seed(42)
random.seed(42)

# generate users
N_USERS = 50000

cities = ['Jakarta', 'Surabaya', 'Bandung', 'Yogyakarta', 'Medan']
city_probs = [0.35, 0.20, 0.20, 0.15, 0.10]

devices = ['Android', 'iOS']
device_probs = [0.75, 0.25]

segments = ['New', 'Returning', 'Power']
segment_probs = [0.40, 0.45, 0.15]

base_date = datetime(2026, 1, 1)

users = []

for i in range(1, N_USERS + 1):
    user_id = f'U{i:06d}'

    city = np.random.choice(cities, p=city_probs)
    device = np.random.choice(devices, p=device_probs)
    segment = np.random.choice(segments, p=segment_probs)

    signup_days_ago = np.random.randint(1, 730)
    signup_date = base_date - timedelta(days=int(signup_days_ago))

    if segment == 'New':
        total_completed_rides = np.random.randint(0, 5)
    elif segment == 'Returning':
        total_completed_rides = np.random.randint(5, 50)
    else:
        total_completed_rides = np.random.randint(50, 300)

    users.append([
        user_id,
        signup_date.date(),
        city,
        device,
        segment,
        total_completed_rides
    ])

users_df = pd.DataFrame(
    users,
    columns=[
        'user_id',
        'signup_date',
        'city',
        'device_type',
        'user_segment',
        'total_completed_rides'
    ]
)

os.makedirs("data/raw", exist_ok=True)
users_df.to_csv("data/raw/users.csv", index=False)

print(users_df.head())
print(f"Total users generated: {len(users_df)}")

# generate sessions
sessions = []

session_counter = 1

for _, user in users_df.iterrows():
    segment = user['user_segment']

    if segment == 'New':
        n_sessions = np.random.randint(1, 4)
    elif segment == 'Returning':
        n_sessions = np.random.randint(4, 13)
    else:
        n_sessions = np.random.randint(15, 41)
    

    for _ in range(n_sessions):
        session_id = f'S{session_counter:07d}'
        session_counter += 1

        days_offset = np.random.randint(0, 90)
        minutes_offset = np.random.randint(0, 1440)

        session_start = (
            datetime(2026, 1, 1)
            + timedelta(days=int(days_offset), minutes=int(minutes_offset))
        )

        sessions.append([
            session_id,
            user['user_id'],
            session_start,
            user['city'],
            user['device_type'],
            user['user_segment']
        ])

# convert to dataframe
sessions_df = pd.DataFrame(
    sessions,
    columns=[
        'session_id',
        'user_id',
        'session_start',
        'city',
        'device_type',
        'user_segment'
    ]
)

sessions_df.to_csv("data/raw/ride_sessions.csv", index=False)

print(sessions_df.head())
print(f"Total sessions generated: {len(sessions_df)}")

# generate ride events
events = []
event_counter = 1

for _, session in sessions_df.iterrows():
    session_id = session['session_id']
    user_id = session['user_id']
    base_time = pd.to_datetime(session['session_start'])
    
    segment = session['user_segment']

    if segment == 'New':
        p_destination = 0.80
        p_fare = 0.94
        p_request = 0.55
        p_driver = 0.80
        p_complete = 0.90
    
    elif segment == 'Returning':
        p_destination = 0.88
        p_fare = 0.95
        p_request = 0.68
        p_driver = 0.82
        p_complete = 0.93

    else: #Power
        p_destination = 0.96
        p_fare = 0.99
        p_request = 0.90
        p_driver = 0.90
        p_complete = 0.97

    session_events = ['app_open']

    if np.random.rand() < p_destination:
        session_events.append('destination_selected')

        if np.random.rand() < p_fare:
            session_events.append('fare_shown')

            if np.random.rand() < p_request:
                session_events.append('ride_requested')

                if np.random.rand() < p_driver:
                    session_events.append('driver_assigned')

                    if np.random.rand() < p_complete:
                        session_events.append('ride_completed')

    for step, event_name in enumerate(session_events):
        event_id = f'E{event_counter:08d}'
        event_counter += 1

        event_time = base_time + timedelta(seconds=step * 30)

        events.append([
            event_id,
            session_id,
            user_id,
            event_name,
            event_time
        ])

# convert to dataframe
events_df = pd.DataFrame(
    events,
    columns=[
        'event_id',
        'session_id',
        'user_id',
        'event_name',
        'event_time'
    ]
)

events_df.to_csv("data/raw/ride_events.csv", index=False)

print(events_df.head())
print(f"Total events generated: {len(events_df)}")
