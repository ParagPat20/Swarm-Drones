# Connect WiFi
# Create HTML Server
# Beeps - Server Created
# Send / Receive Response - Beeps - Brain Connected
# Connect Drones
# Tune
# Get Vehicle Stats
# Upload all vehicle stats on Server
    # Take ch1out, ch2out, ch3out, ch4out from Client Drone
    # Give channel outs to Copy Drone
# # Waiting for the command from Master..... //Optional
# Arm the Drones //Ready to Flight
# Arm and Take Off // 5m
# Go Forward // 5m
# Go Left // 5m
# Go Right // 5m
# Go Backward // 5m
# Land
# Completion Tune

from __future__ import print_function
from dronekit import connect, VehicleMode
from pymavlink import mavutil # Needed for command message definitions
from my_vehicle import MyVehicle
import time
import math
import socket

def WiFi():
    print("WiFi Connected")

def Create_server():
    print("Server Created")

def send(data,ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(data.encode())
    response = sock.recv(1024)
    print("Response from server:", response.decode())

def send_chout(vehicle,arduino_ip,arduino_port):
    """
    Continuously send data to the Arduino.
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))  # Bind to any available port

    while True:
        try:
            # Connect the socket to the Arduino
            sock.connect((arduino_ip, arduino_port))

            # Get the servo outputs from the client vehicle
            servo_data = {
                'ch1out': vehicle.raw_servo.ch1out,
                'ch2out': vehicle.raw_servo.ch2out,
                'ch3out': vehicle.raw_servo.ch3out,
                'ch4out': vehicle.raw_servo.ch4out
            }

            # Combine the servo outputs into a single string
            data = ",".join(str(value) for value in servo_data.values())

            # Send the data to the Arduino
            sock.sendto(data.encode(), (arduino_ip, arduino_port))

        except Exception as e:
            print("Error sending data:", str(e))

        # Sleep for a short time before sending the next data point
        time.sleep(0.1)
    


def receive(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    

def Tune():
    print("Tune")

def Beep():
    print("Beep")

def connectall(mcu_address, cd_address, sd_address,link,link_port):
    
    MCU = connect(mcu_address, wait_ready = True)
    Beep()
    send("MCU Connected",link,link_port)
    CD = connect(cd_address, wait_ready = True, vehicle_class=MyVehicle)
    Beep()
    send("CD Connected",link,link_port)
    SD = connect(sd_address, wait_ready = True)
    Beep()
    send("SD Connected",link,link_port)

    time.sleep(2)
    send("All Vehicle Connected successfully",link,link_port)

def VehicleStats(vehicle):
    print(" Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" GPS: %s" % vehicle.gps_0)
    print("Vehicle Stats are these")
    print(" Is Armable?: %s" % vehicle.is_armable)
    print(" System status: %s" % vehicle.system_status.state)

def chout(vehicle):
    return (vehicle._raw_servo.ch1out, vehicle._raw_servo.ch2out, vehicle._raw_servo.ch3out, vehicle._raw_servo.ch4out)
    
def command():
    print("Master has sent a command")

def arm(vehicle):
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)
    print("Vehicle Armed")

def TakeOff(vehicle,aTargetAltitude):

    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust = thrust, vehicle=vehicle)
        time.sleep(0.2)

def send_attitude_target(roll_angle=0.0, pitch_angle=0.0,
                         yaw_angle=None, yaw_rate=0.0, use_yaw_rate=False,
                         thrust=0.5, vehicle=None):
    
    if yaw_angle is None:
        # this value may be unused by the vehicle, depending on use_yaw_rate
        yaw_angle = vehicle.attitude.yaw
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    msg = vehicle.message_factory.set_attitude_target_encode(
        0,  # time_boot_ms
        1,  # Target system
        1,  # Target component
        0b00000000 if use_yaw_rate else 0b00000100,
        to_quaternion(roll_angle, pitch_angle, yaw_angle),  # Quaternion
        0,  # Body roll rate in radian
        0,  # Body pitch rate in radian
        math.radians(yaw_rate),  # Body yaw rate in radian/second
        thrust  # Thrust
    )
    vehicle.send_mavlink(msg)


def set_attitude(roll_angle=0.0, pitch_angle=0.0,
                 yaw_angle=None, yaw_rate=0.0, use_yaw_rate=False,
                 thrust=0.5, duration=0, vehicle=None):

    send_attitude_target(roll_angle, pitch_angle,
                         yaw_angle, yaw_rate, False,
                         thrust, vehicle=vehicle)
    start = time.time()
    while time.time() - start < duration:
        send_attitude_target(roll_angle, pitch_angle,
                             yaw_angle, yaw_rate, False,
                             thrust, vehicle=vehicle)
        time.sleep(0.1)
    # Reset attitude, or it will persist for 1s more due to the timeout
    send_attitude_target(0, 0,
                         0, 0, True,
                         thrust, vehicle=vehicle)


def to_quaternion(roll=0.0, pitch=0.0, yaw=0.0):
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

def move_forward(vehicle, duration, distance):
    """
    Move vehicle forward for a specified duration and distance.
    """
    speed = distance / duration
    pitch_angle = -speed
    set_attitude(pitch_angle=pitch_angle, duration=duration, vehicle=vehicle)

def move_backward(vehicle, duration, distance):
    """
    Move vehicle backward for a specified duration and distance.
    """
    speed = distance / duration
    pitch_angle = speed
    set_attitude(pitch_angle=pitch_angle, duration=duration, vehicle=vehicle)

def move_left(vehicle, duration, distance):
    """
    Move vehicle left for a specified duration and distance.
    """
    speed = distance / duration
    roll_angle = speed
    set_attitude(roll_angle=roll_angle, duration=duration, vehicle=vehicle)

def move_right(vehicle, duration, distance):
    """
    Move vehicle right for a specified duration and distance.
    """
    speed = distance / duration
    roll_angle = -speed
    set_attitude(roll_angle=roll_angle, duration=duration, vehicle=vehicle)

def disarm(vehicle):
    print("Disrming motors")
    vehicle.armed = False

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = False
        time.sleep(1)
    print("Vehicle Armed")

def land(vehicle):
    vehicle.mode = VehicleMode("LAND")
    print("Landing")

def exit(vehicle):
    vehicle.close()
    print("Completed")
