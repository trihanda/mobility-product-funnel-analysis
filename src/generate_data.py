import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

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