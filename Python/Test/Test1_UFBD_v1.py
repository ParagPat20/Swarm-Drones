
import time

class DeadReckoning:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.home_location = vehicle.location.global_relative_frame
        self.current_location = [0, 0, 0]
        self.last_time = time.time()

    def update(self):
        # Get the current time
        current_time = time.time()

        # Calculate the time delta
        dt = current_time - self.last_time

        # Update the last time
        self.last_time = current_time

        # Get the current velocity
        velocity = self.vehicle.velocity

        # Update the current location
        self.current_location[0] += velocity[0] * dt
        self.current_location[1] += velocity[1] * dt
        self.current_location[2] += velocity[2] * dt

    def get_location(self):
        return self.current_location

# Connect to the drone
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# Create a DeadReckoning object
dr = DeadReckoning(vehicle)

# Continuously update the dead reckoning position
while True:
    dr.update()
    print("Current location:", dr.get_location())
    time.sleep(0.1)


def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

        
# Set up velocity mappings
# velocity_x > 0 => fly North
# velocity_x < 0 => fly South
# velocity_y > 0 => fly East
# velocity_y < 0 => fly West
# velocity_z < 0 => ascend
# velocity_z > 0 => descend
SOUTH=-2
UP=-0.5   #NOTE: up is negative!

#Fly south and up.
send_ned_velocity(SOUTH,0,UP,DURATION)


# Disconnect from the drone
vehicle.close()


import time
from dronekit import connect, VehicleMode
from pymavlink import mavutil

class DeadReckoning:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.home_location = vehicle.location.global_relative_frame
        self.current_location = [0, 0, 0]
        self.last_time = time.time()

    def update(self):
        # Get the current time
        current_time = time.time()

        # Calculate the time delta
        dt = current_time - self.last_time

        # Update the last time
        self.last_time = current_time

        # Get the current velocity
        velocity = self.vehicle.velocity

        # Update the current location
        self.current_location[0] += velocity[0] * dt
        self.current_location[1] += velocity[1] * dt
        self.current_location[2] += velocity[2] * dt

    def get_location(self):
        return self.current_location

# Connect to the drone
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# Create a DeadReckoning object
dr = DeadReckoning(vehicle)

# Set up velocity mappings
# velocity_x > 0 => fly North
# velocity_x < 0 => fly South
# velocity_y > 0 => fly East
# velocity_y < 0 => fly West
# velocity_z < 0 => ascend
# velocity_z > 0 => descend
SOUTH = -2
UP = -0.5   # NOTE: up is negative!
DURATION = 5  # Specify the duration in seconds

# Set the duration for sending velocity commands
send_velocity_duration = 10  # Specify the duration in seconds

# Start the timer for velocity commands
start_time = time.time()

# Continuously update the dead reckoning position and send velocity commands for a specific duration
while True:
    dr.update()
    print("Current location:", dr.get_location())
    time.sleep(0.1)

    # Check if the duration for sending velocity commands has passed
    if time.time() - start_time > send_velocity_duration:
        # Fly south and up.
        send_ned_velocity(SOUTH, 0, UP, DURATION)
        
        # Reset the timer
        start_time = time.time()

# Disconnect from the drone
vehicle.close()