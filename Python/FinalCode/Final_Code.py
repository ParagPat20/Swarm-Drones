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

from functions import *
import threading
from threading import Thread
mcu_address = '0.0.0.0:14552'
cd_address = '0.0.0.0:14550'
sd_address = 'COM17'
link = "192.168.4.2"
link_port = 8888

from functions import start_server
server_thread = threading.Thread(target=start_server)
server_thread.start()

MCU = connect(mcu_address, wait_ready = True)
Beep(4,0.1)
send("MCU Connected")
CD = connect(cd_address, wait_ready = True)
Beep(4,0.2)
send("CD Connected")
SD = connect(sd_address, wait_ready = True)
Beep(4,0.3)
send("SD Connected")

time.sleep(2)
send("All Vehicle Connected successfully")
Tune()

VehicleStats(MCU)
VehicleStats(CD)
VehicleStats(SD)

def run_commands(vehicle, commands):
    for command in commands:
        command(vehicle)

mcu_commands = [lambda v:arm(v,mode = "GUIDED_NOGPS"),lambda v: time.sleep(10), land, exit]
cd_commands = [lambda v:arm(v,mode = "GUIDED_NOGPS"), lambda v: time.sleep(10), land, exit]
sd_commands = [lambda v:arm(v,mode = "GUIDED_NOGPS"),lambda v: time.sleep(10), land, exit]

mcu_thread = threading.Thread(target=run_commands, args=(MCU, mcu_commands))
cd_thread = threading.Thread(target=run_commands, args=(CD, cd_commands))
sd_thread = threading.Thread(target=run_commands, args=(SD, sd_commands))

mcu_thread.start()
cd_thread.start()
sd_thread.start()

Tune()