# Connect WiFi
# Create HTML Server
# Beeps - Server Created
# Send / Receive Response - Beeps - Brain Connected
# Connect Drones
# Tune
# Get Vehicle Stats
# Upload all vehicle stats on Server
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
import time
import math
import http.client
import json
import http.server
import socketserver
from machine import Pin, PWM

messages = []

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable logging of requests
        pass

    def do_POST(self):
        if self.path == '/Terminal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            message = data['message']
            messages.append(message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/fetch_messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_body = json.dumps({'messages': messages})
            self.wfile.write(response_body.encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('c:/Users/HP/OneDrive/Desktop/Server_test/index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

def start_server(port=8888):
    print("Starting server...")
    handler = MyRequestHandler
    with socketserver.TCPServer(('0.0.0.0', port), handler) as httpd:
        httpd.serve_forever()

def send(*args, ip='192.168.13.101', port=8888):
    message = ' '.join(str(arg) for arg in args)  # Concatenate the arguments into a single message
    conn = http.client.HTTPConnection(ip, port)
    headers = {'Content-type': 'application/json'}
    body = json.dumps({'message': message})
    conn.request('POST', '/Terminal', body, headers)
    response = conn.getresponse()
    print("Response from server:", response.read().decode())

def WiFi():
    print("WiFi Connected")

def Tune():
    notes = [262, 294, 330, 349, 392, 440, 494, 523]

    buzzer = PWM(Pin(15))
    for note in notes:
        buzzer.freq(note)
        buzzer.duty_u16(1000)
        time.sleep(2)
    buzzer.duty_u16(0)

    print("Tune")

def Beep(number, time_gap):
    buzzer = PWM(Pin(15))
    for i in range(number):
        buzzer.on()
        time.sleep(time_gap)
        buzzer.off()
        time.sleep(time_gap)

def VehicleStats(vehicle):
    print(" Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" GPS: %s" % vehicle.gps_0)
    print("Vehicle Stats are these")
    print(" Is Armable?: %s" % vehicle.is_armable)
    print(" System status: %s" % vehicle.system_status.state)
    

def command():
    print("Master has sent a command")

def arm(vehicle):
    print("Arming motors")
    send("Arming Motors")
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        send("waiting for Arming...")
        vehicle.armed = True
        time.sleep(1)
    print("Vehicle Armed")

def TakeOff(vehicle, aTargetAltitude):

    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    thrust = DEFAULT_TAKEOFF_THRUST
    vehicle_name = str(vehicle)
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        send(vehicle_name + " Altitude =", current_altitude)  # Include vehicle name in the message
        if current_altitude >= aTargetAltitude * 0.95:
            print(vehicle_name + " Reached target altitude")
            send(vehicle_name + " Reached the desired Altitude")
            break
        elif current_altitude >= aTargetAltitude * 0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust=thrust, vehicle=vehicle)
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
    send("Landing")

def exit(vehicle):
    vehicle.close()
    print("Completed")
    send("Completed")
