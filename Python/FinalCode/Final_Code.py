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

import threading
import time
from dronekit import connect
from functions import start_server, Beep, send, Copter

mcu_address = 'tcp:127.0.0.1:5762'
cd_address = '0.0.0.0:14550'
sd_address = 'COM17'
link = "192.168.4.2"
link_port = 8888

server_thread = threading.Thread(target=start_server)
server_thread.start()

MCU = connect(mcu_address, wait_ready=True)
mcu = Copter(MCU)
Beep(4, 0.1)
send("MCU Connected")

CD = connect(cd_address, wait_ready=True)
cd = Copter(CD)
Beep(4, 0.2)
send("CD Connected")

SD = connect(sd_address, wait_ready=True)
sd = Copter(SD)
Beep(4, 0.3)
send("SD Connected")

time.sleep(2)
send("All Vehicles Connected successfully")

def run_mcu():
    mcu.arm(mode="GUIDED_NOGPS")
    mcu.takeoff(10)
    mcu.move_forward(3, 10)
    mcu.move_left(10, 10)
    mcu.move_backward(10, 10)
    mcu.land()
    mcu.disarm()
    mcu.exit()

def run_cd():
    cd.arm(mode="GUIDED_NOGPS")
    time.sleep(10)
    cd.land()
    cd.exit()

def run_sd():
    sd.arm(mode="GUIDED_NOGPS")
    time.sleep(10)
    sd.land()
    sd.exit()

mcu_thread = threading.Thread(target=run_mcu)
cd_thread = threading.Thread(target=run_cd)
sd_thread = threading.Thread(target=run_sd)

mcu_thread.start()
cd_thread.start()
sd_thread.start()
