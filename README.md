# Optimizing Ride Booking Conversion: Funnel Analysis for a Mobility App


## Project Overview

**SwiftRide** is a fictional ride-hailing platform operating across multiple cities in Indonesia.

Over the last quarter, the product team observed that overall ride completion rate declined from **72% to 61%**, despite relatively stable app traffic. This indicates growing friction somewhere in the ride-booking journey, potentially affecting revenue, marketplace efficiency, and customer retention.

This project analyzes the end-to-end ride-booking funnel to identify major drop-off points, understand behavioral differences across user segments, and evaluate whether product interventions can improve conversion.

---

## Business Problem

SwiftRide's Product Manager observed that fewer ride-booking sessions are converting into completed rides, even though top-of-funnel traffic remains stable.

This raises several business concerns:

- Reduced completed rides may directly impact revenue and GMV
- Higher booking abandonment may indicate pricing or supply-side friction
- Poor booking experience may increase user churn over time

The analytics team is tasked with investigating:

- Where is the biggest drop-off in the ride-booking funnel?
- Which user segments are most affected?
- How do ETA and surge pricing influence conversion behavior?
- Can product experiments improve booking conversion?

The ultimate goal is to generate data-driven recommendations that improve ride completion and user experience.

---

## Business Questions

This project aims to answer the following questions:

1. What is the overall ride-booking funnel conversion rate?
2. Which funnel stage has the highest drop-off?
3. Which user segments are most likely to abandon the booking process?
4. How do ETA and surge pricing affect conversion behavior?
5. Can product experiments improve booking conversion?

---

## Ride Booking Funnel

The booking journey is modeled as the following funnel:

```text
App Open
   ↓
Destination Selected
   ↓
Fare Shown
   ↓
Ride Requested
   ├── Booking Cancelled
   ↓
Driver Assigned
   ├── Booking Cancelled
   ↓
Ride Completed
```

---

## Dataset

This project uses a synthetic relational dataset generated using Python.

Dataset size:

* 50,000 users
* 425,746 ride sessions
* 2,304,820 ride events
* 120,786 experiment records

---

## Dataset Schema

This project uses four relational tables representing user-level, session-level, event-level, and experiment-level activity.

Each table is connected through user-level and session-level identifiers, enabling funnel tracking from user acquisition to ride completion and experiment evaluation.

### 1. `users.csv` (User-level table)

Stores user profile and historical ride activity.

| Column                | Type     | Description                             |
| --------------------- | -------- | --------------------------------------- |
| user_id               | string   | Unique identifier for each user         |
| signup_date           | date     | Registration date                       |
| city                  | category | User's primary operating city           |
| device_type           | category | Mobile operating system (Android / iOS) |
| user_segment          | category | User segment (New / Returning / Power)  |
| total_completed_rides | integer  | Historical completed rides              |

**Primary Key:** `user_id`

---

### 2. `ride_sessions.csv` (Session-level table)

Represents each booking session.

| Column           | Type     | Description                             |
| ---------------- | -------- | --------------------------------------- |
| session_id       | string   | Unique session identifier               |
| user_id          | string   | Associated user                         |
| session_start    | datetime | Session start timestamp                 |
| city             | category | City where the booking session occurred |
| device_type      | category | Device used                             |
| user_segment     | category | User segment                            |
| eta_minutes      | integer  | Estimated driver pickup time            |
| surge_multiplier | float    | Dynamic pricing multiplier              |
| estimated_fare   | integer  | Estimated fare shown to user            |
| is_peak_hour     | boolean  | Peak demand indicator                   |

**Primary Key:** `session_id`

**Foreign Key:**

* `user_id → users.user_id`

---

### 3. `ride_events.csv` (Event-level table)

Contains event logs for each funnel step.

| Column     | Type     | Description             |
| ---------- | -------- | ----------------------- |
| event_id   | string   | Unique event identifier |
| session_id | string   | Associated session      |
| user_id    | string   | Associated user         |
| event_name | category | Funnel event type       |
| event_time | datetime | Event timestamp         |

**Primary Key:** `event_id`

**Foreign Keys:**

* `session_id → ride_sessions.session_id`
* `user_id → users.user_id`

---

### 4. `experiments.csv` (Experiment-level table)

Contains A/B testing assignments for pricing experiments.
Only sessions with `surge_multiplier >= 1.3` are included in the pricing experiment.

| Column               | Type         | Description                               |
| -------------------- | ------------ | ----------------------------------------- |
| experiment_id        | string       | Unique experiment identifier              |
| session_id           | string       | Associated booking session                |
| variant              | category     | Control / Treatment group                 |
| discount_badge_shown | boolean      | Whether pricing incentive badge is shown  |
| conversion           | integer(0/1) | Whether session converted to ride request |

**Primary Key:** `experiment_id`

**Foreign Key:**
- `session_id → ride_sessions.session_id`

---

## Funnel Event Definitions

| Event                | Description                                             |
| -------------------- | ------------------------------------------------------- |
| app_open             | User opens the SwiftRide app                            |
| destination_selected | User selects pickup/drop-off location                   |
| fare_shown           | Fare estimate is displayed                              |
| ride_requested       | User confirms ride request                              |
| driver_assigned      | Driver accepts booking                                  |
| ride_completed       | Ride successfully completed                             |
| booking_cancelled    | User abandons or cancels booking before ride completion |


---

## Current Progress

- [x] Project setup
- [x] Synthetic data generation (v2)
- [x] Dataset validation
- [ ] Funnel analysis
- [ ] Segment analysis
- [ ] Device & city analysis
- [ ] ETA impact analysis
- [ ] Surge pricing analysis
- [ ] A/B testing evaluation
- [ ] Final business recommendations

---

## Tech Stack

- Python (Pandas, NumPy, Matplotlib)
- SQL
- Jupyter Notebook
- Tableau
- Git / GitHub

---

## Analytical Scope

1. Funnel Analysis  
2. Segment Analysis  
3. Device & City Analysis  
4. ETA Impact Analysis  
5. Surge Pricing Analysis  
6. A/B Testing Evaluation  

---

## Project Deliverables

- Synthetic data generator
- Exploratory data analysis notebook
- SQL analysis queries
- Tableau dashboard
- Business recommendations
