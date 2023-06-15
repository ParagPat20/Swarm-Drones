from dronekit import connect, VehicleMode, LocationGlobalRelative, Vehicle
from pymavlink import mavutil
import time
import threading
import socket
import argparse

# Arduino IP address and port
arduino_ip = "192.168.4.3"  # Replace with your Arduino's IP address
arduino_port = 8888  # Replace with the port your Arduino is listening on

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))  # Bind to any available port

# Connect the socket to the Arduino
sock.connect((arduino_ip, arduino_port))

class RawSERVO(object):
    """
    Class to represent servo outputs.
    """

    def __init__(self, ch1out=None, ch2out=None, ch3out=None, ch4out=None):
        """
        RawSERVO object constructor.
        """
        self.ch1out = ch1out
        self.ch2out = ch2out
        self.ch3out = ch3out
        self.ch4out = ch4out

    def __str__(self):
        """
        String representation used for printing.
        """
        return "{},{},{},{}".format(self.ch1out, self.ch2out, self.ch3out, self.ch4out)


class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)

        # Create a Vehicle.raw_servo object with initial values set to None.
        self._raw_servo = RawSERVO()

        # Create a message listener using the decorator.
        @self.on_message('SERVO_OUTPUT_RAW')
        def listener(self, name, message):
            """
            The listener is called for messages that contain the string specified in the decorator,
            passing the vehicle, message name, and the message.

            The listener writes the message to the (newly attached) ``vehicle.raw_servo`` object
            and notifies observers.
            """
            self._raw_servo.ch1out = message.servo1_raw
            self._raw_servo.ch2out = message.servo2_raw
            self._raw_servo.ch3out = message.servo3_raw
            self._raw_servo.ch4out = message.servo4_raw

            # Notify all observers of the new message (with the updated value)
            #   Note that argument `cache=False` by default so listeners
            #   are updated with every new message
            self.notify_attribute_listeners('raw_servo', self._raw_servo)

    @property
    def raw_servo(self):
        return self._raw_servo


def send_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z, duration):
    """
    Move the vehicle in a direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        velocity_x, velocity_y, velocity_z,
        0, 0, 0,
        0, 0
    )

    for _ in range(duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


def send_data(vehicle):
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

    # Close the socket
    sock.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode')
    parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()

    connection_string = args.connect
    sitl = None

    # Start SITL if no connection string is specified
    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    client = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)
    print("Client connected")

    # Arm the client vehicle
    client.mode = VehicleMode("GUIDED_NOGPS")
    client.armed = True
    while not client.armed:
        time.sleep(1)

    # Start data sending thread
    data_thread = threading.Thread(target=send_data, args=(client,))
    data_thread.start()

    # Move forward for 5 seconds
    send_ned_velocity(client, 5, 0, 0, 5)

    # Move backward for 5 seconds
    send_ned_velocity(client, -5, 0, 0, 5)

    # Disarm the client vehicle
    client.armed = False
    while client.armed:
        time.sleep(1)

    print("Completed")
    client.close()
    sock.close()

# from dronekit import connect, VehicleMode, LocationGlobalRelative, Vehicle
# from pymavlink import mavutil
# import time
# import requests
# import threading

# class MyVehicle(Vehicle):
#     def __init__(self, *args):
#         super(MyVehicle, self).__init__(*args)

#         # Create an Vehicle.raw_servo object with initial values set to None.
#         self._raw_servo = self.RawSERVO()

#         # Create a message listener using the decorator.   
#         @self.on_message('SERVO_OUTPUT_RAW')
#         def listener(self, name, message):
#             """
#             The listener is called for messages that contain the string specified in the decorator,
#             passing the vehicle, message name, and the message.
            
#             The listener writes the message to the (newly attached) ``vehicle.raw_servo`` object 
#             and notifies observers.
#             """
#             self._raw_servo.ch1out=message.servo1_raw
#             self._raw_servo.ch2out=message.servo2_raw
#             self._raw_servo.ch3out=message.servo3_raw
#             self._raw_servo.ch4out=message.servo4_raw

#             # Notify all observers of new message (with new value)
#             #   Note that argument `cache=False` by default so listeners
#             #   are updated with every new message
#             self.notify_attribute_listeners('raw_servo', self._raw_servo) 

#     @property
#     def raw_servo(self):
#         return self._raw_servo
    
#     class RawSERVO(object):
#         """
#         :param ch1out: servo1
#         :param ch2out: servo2
#         :param ch3out: servo3
#         :param ch4out: servo4
#         """
#         def __init__(self, ch1out=None, ch2out=None, ch3out=None, ch4out=None):
#             """
#             RawIMU object constructor.
#             """
#             self.ch1out = ch1out
#             self.ch2out = ch2out
#             self.ch3out = ch3out
#             self.ch4out = ch4out

#         def __str__(self):
#             """
#             String representation used to print 
#             """
#             return "{},{},{},{}".format(self.ch1out, self.ch2out, self.ch3out, self.ch4out)

# # Connect to MCU (Vehicle 1) using MyVehicle class

# #mcu = connect('COM3', wait_ready=True, vehicle_class=MyVehicle)
# #print("MCU Connected")

# # Connect to Client (Vehicle 2) using MyVehicle class
# client = connect('0.0.0.0:14550', wait_ready=True, vehicle_class=MyVehicle)
# print("CLIENT connected")

# # Arm MCU (Vehicle 1)
# #mcu.mode = VehicleMode("GUIDED_NOGPS")
# #mcu.armed = True
# #while not mcu.armed:
#     #time.sleep(1)

# # Arm Client (Vehicle 2)
# client.mode = VehicleMode("GUIDED_NOGPS")
# client.armed = True
# while not client.armed:
#     time.sleep(1)

# def send_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z, duration):
#     """
#     Move vehicle in direction based on specified velocity vectors.
#     """
#     msg = vehicle.message_factory.set_position_target_local_ned_encode(
#         0,
#         0, 0,
#         mavutil.mavlink.MAV_FRAME_LOCAL_NED,
#         0b0000111111000111,
#         0, 0, 0,
#         velocity_x, velocity_y, velocity_z,
#         0, 0, 0,
#         0, 0)
#     for x in range(0,duration):
#         vehicle.send_mavlink(msg)
#         time.sleep(1)

# def send_data():
#     """
#     Continuously send data to web server.
#     """
#     while True:
#         try:
#             # Get RPM data from client vehicle using raw_servo attribute
#             RPM = {
#                 'ch1out': client.raw_servo.ch1out,
#                 'ch2out': client.raw_servo.ch2out,
#                 'ch3out': client.raw_servo.ch3out,
#                 'ch4out': client.raw_servo.ch4out
#             }

#             # Send RPM data to web server
#             r = requests.post(url, RPM)

#         except Exception as e:
#             print("Error sending data:", str(e))

#         # Sleep for a short time before sending the next data point
#         time.sleep(0.1)

# # Start data sending thread
# data_thread = threading.Thread(target=send_data)
# data_thread.start()

# # Move forward for 5 seconds
# send_ned_velocity(client, 5, 0, 0, 5)

# # Move backward for 5 seconds
# send_ned_velocity(client, -5, 0, 0, 5)

# # Disarm MCU (Vehicle 1)
# #mcu.armed = False
# #while mcu.armed:
#     #time.sleep(1)

# # Disarm Client (Vehicle 2)
# client.armed = False
# while client.armed:
#     time.sleep(1)

# print("Completed")
# client.close()