import datetime
import random

from django.utils.timezone import now
from ride_share_app.models import UserAccount, Ride, RideEvent
from django.contrib.auth.models import User

# Helper Functions
def create_user(username, email, password, first_name, last_name, role):
    id = random.randint(0, 999)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user_account = UserAccount.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=f'+639950074{id}',
        role=role
    )
    return user_account

def create_ride(status, rider, driver, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, pickup_time):
    return Ride.objects.create(
        status=status,
        id_rider=rider,
        id_driver=driver,
        pickup_latitude=pickup_lat,
        pickup_longitude=pickup_lon,
        dropoff_latitude=dropoff_lat,
        dropoff_longitude=dropoff_lon,
        pickup_time=pickup_time
    )

def create_ride_event(ride, description):
    return RideEvent.objects.create(
        id_ride=ride,
        description=description)

# Populating Data
def populate_initial_data():
    id = random.randint(0, 99)

    # Create Admin User
    create_user(
        username=f'admin{id}',
        email=f'admin{id}@gmail.com',
        password='thisisapassword',
        first_name='Admin',
        last_name='User',
        role='admin'
    )

    # Create Rider and Driver Users
    rider = create_user(
        username=f'rider{id}',
        email=f'rider{id}@gmail.com',
        password='thisisapassword',
        first_name='John',
        last_name=f'Doe{id}',
        role='rider'
    )

    driver = create_user(
        username=f'driver{id}',
        email=f'driver{id}@gmail.com',
        password='thisisapassword',
        first_name='Jane',
        last_name=f'Smith{id}',
        role='driver'
    )

    # Create a Ride
    ride = create_ride(
        status='en-route',
        rider=rider,
        driver=driver,
        pickup_lat=12.971598,
        pickup_lon=77.594566,
        dropoff_lat=12.295810,
        dropoff_lon=76.639381,
        pickup_time=now() - datetime.timedelta(hours=1)
    )

    # Create Ride Events
    create_ride_event(ride, description='Status changed to pickup')
    create_ride_event(ride, description='Status changed to dropoff')

    print('Sample data populated successfully.')

