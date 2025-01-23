# Django Project README

## Project Overview

This project implements a RESTful API for managing ride information using the Django framework and Django REST Framework (DRF). The application provides functionalities such as user authentication, ride event tracking, and efficient data retrieval with optimized queries.

---

## Features

- User authentication with role-based access control (admin-only API access).
- CRUD operations for `Ride`, `User`, and `RideEvent` models.
- Filtering, sorting, and pagination for the Ride List API.
- Performance-optimized data retrieval for large datasets.
- Additional field `todays_ride_events` in rides for events occurring in the last 24 hours.
- Minimal SQL queries for better performance.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/lojayrivz/wingz.git
   cd wingz
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv env
   # Activate the virtual environment:
   # On Windows:
   .\env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   Create the database schema by applying migrations:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**
   Create an admin user for accessing the Django Admin panel:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   Start the server and access the application locally:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## API Documentation

### Base URL

- Development: `http://127.0.0.1:8000/app/api/`

### Endpoints

| Method | Endpoint       | Description                                             |
| ------ | -------------- | ------------------------------------------------------- |
| GET    | `/rides/`      | List all rides with filtering, sorting, and pagination. |
| POST   | `/rides/`      | Create a new ride (admin only).                         |
| GET    | `/rides/<id>/` | Retrieve details of a specific ride.                    |
| PUT    | `/rides/<id>/` | Update an existing ride (admin only).                   |
| DELETE | `/rides/<id>/` | Delete a ride (admin only).                             |

| Method | Endpoint       | Description                           |
| ------ | -------------- | ------------------------------------- |
| GET    | `/users/`      | List all user                         |
| POST   | `/users/`      | Create a new user (admin only).       |
| GET    | `/users/<id>/` | Retrieve details of a specific user.  |
| PUT    | `/users/<id>/` | Update an existing user (admin only). |
| DELETE | `/users/<id>/` | Delete a user (admin only).           |

| Method | Endpoint             | Description                                 |
| ------ | -------------------- | ------------------------------------------- |
| GET    | `/ride-events/`      | List all ride events                        |
| POST   | `/ride-events/`      | Create a new ride event (admin only).       |
| GET    | `/ride-events/<id>/` | Retrieve details of a specific ride event.  |
| PUT    | `/ride-events/<id>/` | Update an existing ride event (admin only). |
| DELETE | `/ride-events/<id>/` | Delete a ride event (admin only).           |

---

## Data Population

Populate Data with an Admin, Rider, Driver, Ride and Ride Event

```bash
    python manage.py shell
    from populate_data import populate_initial_data
    populate_initial_data()
```

---

## Design Decisions

- **Authentication:** Implemented role-based access using Django's built-in user model and permissions.
- **Database Optimization:** Used `select_related` and `prefetch_related` to minimize SQL queries.
- **Sorting and Filtering:** Leveraged DRF's filtering and custom sorting mechanisms for efficient data handling.
- **Scalability:** Designed the API to handle large datasets with minimal performance overhead.

---

## Challenges Faced

- Deciding wheter to utilize teh Builtin user Model or use the instructed User Table and create own Authentication Custom Backend. And decided to Modify the User table that was instructed to UserAccount have the builtin Django User Model as its OneToOne Field to utilize Builtin Authentication
- Need more research and analysis on how to Optimize the Queries
- Finding difficulty in calculating the distance, just used simple distance calculation

---

## Raw SQL Query for Reporting

Include the raw SQL query required for calculating trips longer than 1 hour by month and driver:

```sql
SELECT strftime('%Y-%m', r.pickup_time) AS month,
       d.first_name || ' ' || d.last_name AS driver,
       COUNT(*) AS trip_count
FROM ride r
JOIN ride_event e_pickup ON r.id_ride = e_pickup.id_ride AND e_pickup.description = 'Status changed to pickup'
JOIN ride_event e_dropoff ON r.id_ride = e_dropoff.id_ride AND e_dropoff.description = 'Status changed to dropoff'
JOIN user d ON r.id_driver = d.id_user
WHERE (julianday(e_dropoff.created_at) - julianday(e_pickup.created_at)) * 24 > 1
GROUP BY month, driver
ORDER BY month, driver;
```

---
