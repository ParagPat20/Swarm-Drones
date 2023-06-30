from dronekit import connect, VehicleMode
import time
from pymavlink import mavutil
from functions import *

# Connect to the Vehicle
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)

# Set the vehicle to GUIDED mode
vehicle.mode = VehicleMode("GUIDED_NOGPS")

# Arm the vehicle
vehicle.armed = True

# Wait for the vehicle to arm
while not vehicle.armed:
    print("Waiting for vehicle to arm...")
    time.sleep(1)

TakeOff(vehicle,10)

move_forward(vehicle,3,2)
move_left(vehicle,3,2)