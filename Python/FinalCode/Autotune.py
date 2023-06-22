from dronekit import connect, VehicleMode
import time
from pymavlink import mavutil

# Connect to the Vehicle
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)

# Set the vehicle to GUIDED mode
vehicle.mode = VehicleMode("GUIDED")

# Arm the vehicle
vehicle.armed = True

# Wait for the vehicle to arm
while not vehicle.armed:
    print("Waiting for vehicle to arm...")
    time.sleep(1)

# Send MAV_CMD_DO_AUTOTUNE_ENABLE command
vehicle.send_mavlink(vehicle.message_factory.command_long_encode(
    0, 0,  # Target system and target component
    mavutil.mavlink.MAV_CMD_DO_AUTOTUNE_ENABLE,
    0,  # Confirmation
    1,  # Parameter 1: Autotune enable (1 to enable, 0 to disable)
    0,  # Parameter 2: Reserved
    0,  # Parameter 3: Reserved
    0,  # Parameter 4: Reserved
    0,  # Parameter 5: Reserved
    0,  # Parameter 6: Reserved
    0  # Parameter 7: Reserved
))

print("Autotune initiated. Please wait...")

# Wait for the autotuning process to complete
while vehicle.mode.name == "GUIDED":
    print("Autotuning in progress...")
    time.sleep(1)

print("Autotuning completed.")

# Takeoff to a desired altitude
target_altitude = 10  # meters
vehicle.simple_takeoff(target_altitude)

# Wait until the vehicle reaches the target altitude
while vehicle.location.global_relative_frame.alt < target_altitude * 0.95:
    print("Vehicle taking off...")
    time.sleep(1)

print("Vehicle reached target altitude.")

# Fly in autotune mode
vehicle.mode = VehicleMode("AUTOTUNE")

# Keep flying for a certain duration (e.g., 30 seconds)
flight_duration = 30  # seconds
end_time = time.time() + flight_duration

while time.time() < end_time:
    print("Flying in autotune mode...")
    time.sleep(1)

print("Autotune flight completed.")

# Land the vehicle
vehicle.mode = VehicleMode("LAND")

# Wait until the vehicle has landed
while vehicle.mode.name != "LAND":
    print("Vehicle landing...")
    time.sleep(1)

print("Vehicle landed.")

# Disarm the vehicle
vehicle.armed = False

# Close the connection
vehicle.close()
