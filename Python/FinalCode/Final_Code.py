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

from my_vehicle import MyVehicle
from functions import *
import threading

mcu_address = 'tcp:127.0.0.1:5762'
cd_address = 'tcp:127.0.0.1:5772'
# sd_address = 'tcp:127.0.0.1:5782'
link = "192.168.4.2/link"
link_port = 8888
arduino_ip = "192.168.4.2/copy"
arduino_port = 8888

MCU = connect(mcu_address, wait_ready = True)
Beep()
send("MCU Connected",link,link_port)
CD = connect(cd_address, wait_ready = True, vehicle_class=MyVehicle)
Beep()
send("CD Connected",link,link_port)
# SD = connect(sd_address, wait_ready = True)
# Beep()
# send("SD Connected",link,link_port)

time.sleep(2)
# send("All Vehicle Connected successfully",link,link_port)
Tune()

VehicleStats(MCU)
VehicleStats(CD)
# VehicleStats(SD)

TerminalIP = "192.168.4.2/Terminal"
TerminalPort = 8888
read_pipe, write_pipe = os.pipe()
os.dup2(write_pipe, 1)

Terminal_Thread = threading.Thread(target=send_output, args=(read_pipe, send, TerminalIP, TerminalPort))
Terminal_Thread.start()

chout_thread = threading.Thread(target=send_chout, args=(CD, arduino_ip, arduino_port))
chout_thread.start()
ch1out, ch2out, ch3out, ch4out = chout(CD)

def run_commands(vehicle, commands):
    # This is the function that will run in each thread
    for command in commands:
        # Execute the command
        command(vehicle)

# Define the commands for each vehicle
mcu_commands = [arm, lambda v: TakeOff(v, 10), lambda v: move_forward(v, 10, 100), lambda v: move_left(v, 20, 100), lambda v: move_backward(v, 20, 100), lambda v: move_right(v, 20, 100),land]
cd_commands = [arm, lambda v: TakeOff(v, 10), lambda v: move_forward(v, 20, 10), lambda v: move_left(v, 20, 10), lambda v: move_backward(v, 20, 10), lambda v: move_right(v, 20, 10),land]
# sd_commands = [arm, lambda v: TakeOff(v, 10), lambda v: move_forward(v, 20, 10), lambda v: move_left(v, 20, 10), lambda v: move_backward(v, 20, 10), lambda v: move_right(v, 20, 10),land]

# Create a new thread for each vehicle
mcu_thread = threading.Thread(target=run_commands, args=(MCU, mcu_commands))
cd_thread = threading.Thread(target=run_commands, args=(CD, cd_commands))
# sd_thread = threading.Thread(target=run_commands, args=(SD, sd_commands))

# Start the threads
mcu_thread.start()
cd_thread.start()
# sd_thread.start()