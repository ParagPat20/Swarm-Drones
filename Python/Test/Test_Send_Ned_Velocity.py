from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
from dronekit import mavutil


# import argparse  
# parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
# parser.add_argument('--connect', 
#                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
# args = parser.parse_args()

# connection_string = args.connect
# sitl = None


# #Start SITL if no connection string specified
# if not connection_string:
#     import dronekit_sitl
#     sitl = dronekit_sitl.start_default()
#     connection_string = sitl.connection_string()


# # Connect to the Vehicle
# print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    print('\n')
    print('{} - Calling function send_body_frame_velocity(Vx={}, Vy={}, Vz={}, Duration={})'.format(time.ctime(), velocity_x, velocity_y, velocity_z, duration))
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, int(math.ceil(duration))):
        vehicle.send_mavlink(msg)
        print('{} - Body Frame Velocity command is sent! Vx={}, Vy={}, Vz={}'.format(time.ctime(), velocity_x, velocity_y, velocity_z))
        print('{} - Duration = {} seconds'.format(time.ctime(), x+1))
        time.sleep(1)
        print('\n')


def send_attitude_target(roll_angle = 0.0, pitch_angle = 0.0,
                         yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                         thrust = 0.5):

    if yaw_angle is None:
        # this value may be unused by the vehicle, depending on use_yaw_rate
        yaw_angle = vehicle.attitude.yaw
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    msg = vehicle.message_factory.set_attitude_target_encode(
        0, # time_boot_ms
        1, # Target system
        1, # Target component
        0b00000000 if use_yaw_rate else 0b00000100,
        to_quaternion(roll_angle, pitch_angle, yaw_angle), # Quaternion
        0, # Body roll rate in radian
        0, # Body pitch rate in radian
        math.radians(yaw_rate), # Body yaw rate in radian/second
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)

def set_attitude(roll_angle = 0.0, pitch_angle = 0.0,
                 yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                 thrust = 0.5, duration = 0):
    """
    Note that from AC3.3 the message should be re-sent more often than every
    second, as an ATTITUDE_TARGET order has a timeout of 1s.
    In AC3.2.1 and earlier the specified attitude persists until it is canceled.
    The code below should work on either version.
    Sending the message multiple times is the recommended way.
    """
    send_attitude_target(roll_angle, pitch_angle,
                         yaw_angle, yaw_rate, False,
                         thrust)
    start = time.time()
    while time.time() - start < duration:
        send_attitude_target(roll_angle, pitch_angle,
                             yaw_angle, yaw_rate, False,
                             thrust)
        time.sleep(0.1)
    # Reset attitude, or it will persist for 1s more due to the timeout
    send_attitude_target(0, 0,
                         0, 0, True,
                         thrust)
def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
    """
    Convert degrees to quaternions
    """
    t0 = math.cos(math.radians(yaw * 0.5))
    t1 = math.sin(math.radians(yaw * 0.5))
    t2 = math.cos(math.radians(roll * 0.5))
    t3 = math.sin(math.radians(roll * 0.5))
    t4 = math.cos(math.radians(pitch * 0.5))
    t5 = math.sin(math.radians(pitch * 0.5))

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    return [w, x, y, z]
    
#############################################################################################################################################################################

##############################################################_________________ APPLICATION FUNCTIONS_______________________#################################################

def arm_and_takeoff_nogps(desired_altitude):
    DEFAULT_TAKEOFF_THRUST = 1
    SMOOTH_TAKEOFF_THRUST = 0.7

    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    vehicle.armed = True
    print("arming")
    while not vehicle.armed:
        print("Waiting for vehicle to get armed")
        time.sleep(1)
    thrust = DEFAULT_TAKEOFF_THRUST

    while 1:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(current_altitude,desired_altitude)
        if current_altitude >= desired_altitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= desired_altitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust = thrust)
        time.sleep(0.2)

#Arm and take of to altitude of 5 meters
arm_and_takeoff_nogps(5)
send_ned_velocity(0.5,0,0,10)
send_ned_velocity(0,0,0,1)
send_ned_velocity(0,0.5,0,10)
send_ned_velocity(0,0,0,1)
send_ned_velocity(-0.5,0,0,10)
send_ned_velocity(0,0,0,1)
send_ned_velocity(0,-0.5,0,10)
send_ned_velocity(0,0,0,1)

vehicle.mode = VehicleMode("LAND")

vehicle.close()
print("Completed")