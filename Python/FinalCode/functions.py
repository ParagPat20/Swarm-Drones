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
import time

def WiFi():
    print("WiFi Connected")

def Create_server():
    print("Server Created")

def send(data,ip,port):
    print("Data sent on ip:port")

def receive(ip,port):
    print("---- data recieved and saved as variables")

def Tune():
    print("Tune")

def connect():
    
    print("Vehicle Connected")

def VehicleStats():
    print(" Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" GPS: %s" % vehicle.gps_0)
    print("Vehicle Stats are these")

def chout():
    print("chOuts are : ")

def command():
    print("Master has sent a command")

def arm():
    print("Vehicle Armed")

def TakeOff():
    print("Altitude Reached")

def move():
    print("Moving in ....._____")

def land():
    print("Landing")

def exit():
    print("Completed")
