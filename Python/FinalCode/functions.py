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
# from machine import Pin, PWM

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
        elif self.path == '/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            command = data['command']
            # Handle the command
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
            with open('c:/Users/HP/OneDrive/Documents/SwarmDrones/Server_test/index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

def start_server(port=8888):
    print("Starting server...")
    handler = MyRequestHandler
    with socketserver.TCPServer(('0.0.0.0', port), handler) as httpd:
        httpd.serve_forever()

def send(*args, ip='192.168.4.2', port=8888):
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
    # notes = [262, 294, 330, 349, 392, 440, 494, 523]

    # buzzer = PWM(Pin(15))
    # for note in notes:
    #     buzzer.freq(note)
    #     buzzer.duty_u16(1000)
    #     time.sleep(2)
    # buzzer.duty_u16(0)

    print("Tune")

def Beep(number, time_gap):
    # buzzer = PWM(Pin(15))
    # for i in range(number):
    #     buzzer.on()
    #     time.sleep(time_gap)
    #     buzzer.off()
    #     time.sleep(time_gap)
    print("Beep")


class Copter:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def VehicleStats(self):
        print("Vehicle Stats are these")
        print(" Attitude: %s" % self.attitude)
        print(" Velocity: %s" % self.velocity)
        print(" GPS: %s" % self.gps_0)
        print(" Is Armable?: %s" % self.is_armable)
        print(" System status: %s" % self.system_status.state)

    def arm(self,mode):
        print("Arming motors")
        self.vehicle.mode = VehicleMode(mode)
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print("Waiting for arming...")
            self.vehicle.armed = True
            time.sleep(1)
        print("Vehicle Armed")

    def takeoff(self, target_altitude):
        DEFAULT_TAKEOFF_THRUST = 0.7
        SMOOTH_TAKEOFF_THRUST = 0.6

        thrust = DEFAULT_TAKEOFF_THRUST
        while True:
            current_altitude = self.vehicle.location.global_relative_frame.alt
            print("Altitude: %f  Desired: %f" % (current_altitude, target_altitude))
            if current_altitude >= target_altitude * 0.95:
                print(" Reached target altitude")
                break
            elif current_altitude >= target_altitude * 0.6:
                thrust = SMOOTH_TAKEOFF_THRUST
            self.set_attitude(thrust=thrust)
            time.sleep(0.2)

    def send_attitude_target(self, roll_angle=0.0, pitch_angle=0.0,
                             yaw_angle=None, yaw_rate=0.0, use_yaw_rate=False,
                             thrust=0.5):
        if yaw_angle is None:
            yaw_angle = self.vehicle.attitude.yaw

        msg = self.vehicle.message_factory.set_attitude_target_encode(
            0,  # time_boot_ms
            1,  # Target system
            1,  # Target component
            0b00000000 if use_yaw_rate else 0b00000100,
            self.to_quaternion(roll_angle, pitch_angle, yaw_angle),
            0,  # Body roll rate in radian
            0,  # Body pitch rate in radian
            math.radians(yaw_rate),  # Body yaw rate in radian/second
            thrust  # Thrust
        )
        self.vehicle.send_mavlink(msg)

    def set_attitude(self, roll_angle=0.0, pitch_angle=0.0,
                     yaw_angle=None, yaw_rate=0.0, use_yaw_rate=False,
                     thrust=0.5, duration=0):
        self.send_attitude_target(roll_angle, pitch_angle, yaw_angle, yaw_rate,
                                  use_yaw_rate, thrust)
        start = time.time()
        while time.time() - start < duration:
            self.send_attitude_target(roll_angle, pitch_angle, yaw_angle, yaw_rate,
                                      use_yaw_rate, thrust)
            time.sleep(0.1)
        self.send_attitude_target(0, 0,
                         0, 0, True,
                         thrust)

    def to_quaternion(self, roll=0.0, pitch=0.0, yaw=0.0):
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

    def disarm(self):
        print("Disarming motors")
        self.vehicle.armed = False

        while self.vehicle.armed:
            print("Waiting for disarming...")
            self.vehicle.armed = False
            time.sleep(1)
        print("Vehicle Disarmed")

    def land(self):
        self.vehicle.mode = VehicleMode("LAND")
        print("Landing")

    def exit(self):
        self.vehicle.close()
        print("Completed")
