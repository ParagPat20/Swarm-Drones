from dronekit import connect
from my_vehicle import MyVehicle  # assuming the MyVehicle class is defined in a file named my_vehicle.py
import time
from library import *

ip = "192.168.4.2"  # Replace with your Arduino's IP address
port = 8888  # Replace with the port your Arduino is listening on

# Connect the socket to the Arduino
mcu = connect('COM3', wait_ready=True, vehicle_class=MyVehicle)
client = connect('0.0.0.0:14550', wait_ready=True, vehicle_class=MyVehicle)
print("Client Conencted")
send_data(client,ip,port)
# Arm and Takeoff the vehicles
mcu.armed = True
print("MCU Armed")
send_local_ned_velocity(mcu,0,0,-0.5,10)
time.sleep(10)

send_local_ned_velocity(mcu,0.5,0,0,200)
time.sleep(200)

send_local_ned_velocity(mcu,0,0.5,0,200)
time.sleep(200)

send_local_ned_velocity(mcu,-0.5,0,0,200)
time.sleep(200)

send_local_ned_velocity(mcu,0,-0.5,0,200)
time.sleep(200)

send_local_ned_velocity(mcu,0,0,0.5,10)
time.sleep(10)
print("Time up")



client.armed = True
print("Client Armed")

send_local_ned_velocity(client,0,0,-0.5,10)
time.sleep(10)

send_local_ned_velocity(client,0.5,0,0,200)
time.sleep(200)

send_local_ned_velocity(client,0,0.5,0,200)
time.sleep(200)

send_local_ned_velocity(client,-0.5,0,0,200)
time.sleep(200)

send_local_ned_velocity(client,0,-0.5,0,200)
time.sleep(200)

send_local_ned_velocity(client,0,0,0.5,10)
time.sleep(10)
print("Time up")


# Close vehicle objects before exiting the script