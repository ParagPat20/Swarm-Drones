from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
import requests


# Connect to the Vehicle
vehicle = connect('COM17', wait_ready=True)

###########################################################################______________MANDATORY FUNCTIONS_______####################################################


def send_attitude_target(roll_angle = 0.0, pitch_angle = 0.0,
                         yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                         thrust = 0.5):
    """
    use_yaw_rate: the yaw can be controlled using yaw_angle OR yaw_rate.
                  When one is used, the other is ignored by Ardupilot.
    thrust: 0 <= thrust <= 1, as a fraction of maximum vertical thrust.
            Note that as of Copter 3.5, thrust = 0.5 triggers a special case in 
            the code for maintaining current altitude.
    """
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

    vehicle.mode = VehicleMode("GUIDED")
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

#move forward,right,left,backward script
def move_forward(pitch_angle,thrust,duration):
    set_attitude(pitch_angle = -pitch_angle, thrust =thrust, duration = duration)
    #print("moving forward")
def move_backward(pitch_angle,thrust,duration):
    set_attitude(pitch_angle = pitch_angle, thrust = thrust, duration = duration)
    #print("moving backward")
def move_right(roll_angle,thrust,duration):
    set_attitude(roll_angle = roll_angle, thrust = thrust, duration = duration)
    #print("moving right")
def move_left(roll_angle,thrust,duration):
    set_attitude(roll_angle = roll_angle, thrust = thrust, duration = duration)
    #print("moving left")

def Shape_formation():
    move_forward(5,0.5,3)
    move_backward(5,0.5,3)
    move_right(1,0.5,1)


    
    """"
    triangle
    line
    sqaure
    circle
    """


print("arming and taking off")
arm_and_takeoff_nogps(1)
print("shape")
Shape_formation()
time.sleep(50)
vehicle.mode = VehicleMode("LAND")
print("landing")
time.sleep(8)
vehicle.armed = False
vehicle.close()
print("Close vehicle object")