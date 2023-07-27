import threading
import time
from dronekit import connect
from functions import start_server, send, Copter

mcu_address = 'tcp:127.0.0.1:5762'
# cd_address = '0.0.0.0:14550'

# server_thread = threading.Thread(target=start_server)
# server_thread.start()
time.sleep(1)

# send("Connecting to MCU")
print("Connecting to MCU")

MCU = connect(mcu_address, wait_ready=True)
mcu = Copter(MCU)
print("Connected to MCU")
# send("MCU Connected")

# send("Connecting to CD")
print("Connecting to CD")

# CD = connect(cd_address, wait_ready=True)
# cd = Copter(CD)
print("Connected to CD")
# send("CD Connected")

def run_mcu():
    mcu.arm(mode="GUIDED")
    mcu.takeoff(3)
    time.sleep(1)
    mcu.land()
    mcu.disarm()
    mcu.exit()

# def run_cd():
#     cd.arm(mode="GUIDED_NOGPS")
#     time.sleep(2)
#     cd.takeoff(0.3)
#     time.sleep(10)
#     cd.land()
#     cd.disarm()
#     cd.exit()


mcu_thread = threading.Thread(target=run_mcu)
mcu_thread.start()

# cd_thread = threading.Thread(target=run_cd)
# cd_thread.start()
