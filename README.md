# Optimizing Ride Booking Conversion: Funnel Analysis for a Mobility App

## Project Overview

**SwiftRide** is a fictional ride-hailing company operating across multiple cities in Indonesia. Over the last quarter, the product team observed a decline in ride completion rates, indicating potential friction in the booking journey.

This project analyzes the end-to-end ride-booking funnel to identify major drop-off points, understand behavioral differences across user segments, and evaluate whether product interventions can improve conversion rates.

---

## Business Problem

SwiftRide's Product Manager noticed that fewer users are successfully completing rides despite stable app traffic.

The analytics team is asked to investigate:

* Where is the biggest drop-off in the ride-booking funnel?
* Which user segments are most affected?
* Does booking behavior differ across cities or device types?
* Can product experiments improve conversion rates?

The ultimate goal is to generate data-driven recommendations that improve ride completion and user experience.

---

## Business Questions

This project aims to answer the following questions:

1. What is the overall ride-booking funnel conversion rate?
2. Which funnel stage has the highest drop-off?
3. Which user segments are most likely to abandon the booking process?
4. Do city and device type influence conversion behavior?
5. Can product experiments improve conversion rates?

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
   ↓
Driver Assigned
   ↓
Ride Completed
```

---

## Dataset

This project uses a synthetic relational dataset generated using Python.

Dataset size:

* 50,000 users
* 429,119 ride sessions
* 2,003,353 ride events

---

## Dataset Schema

This project uses three relational tables representing user-level, session-level, and event-level activity.

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

| Column        | Type     | Description               |
| ------------- | -------- | ------------------------- |
| session_id    | string   | Unique session identifier |
| user_id       | string   | Associated user           |
| session_start | datetime | Session start timestamp   |
| city          | category | Session city              |
| device_type   | category | Device used               |
| user_segment  | category | User segment              |

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

## Funnel Event Definitions

| Event                | Description                           |
| -------------------- | ------------------------------------- |
| app_open             | User opens the SwiftRide app          |
| destination_selected | User selects pickup/drop-off location |
| fare_shown           | Fare estimate is displayed            |
| ride_requested       | User confirms ride request            |
| driver_assigned      | Driver accepts booking                |
| ride_completed       | Ride successfully completed           |

---

## Current Progress

* [x] Project setup
* [x] Synthetic data generation
* [x] Segment-based funnel validation
* [ ] Funnel analysis
* [ ] Segment analysis
* [ ] Experiment simulation
* [ ] Statistical testing
* [ ] Final business recommendation

---

## Tech Stack

### Core

* Python
* Pandas
* Jupyter Notebook
* Git / GitHub

### Planned Analytics & Visualization

* SQL
* Tableau

---

## Project Deliverables

Planned outputs:

* GitHub repository
* Analytical notebook
* Funnel visualization dashboard
* Business recommendations
