from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
import time
from functions import start_server, Beep, send, Copter


mcu_address = 'tcp:127.0.0.1:5762'

MCU = connect(mcu_address, wait_ready=True)
mcu = Copter(MCU)
time.sleep(2)
def run_mcu():
    mcu.arm()
    mcu.takeoff(10)
    time.sleep(3)
    mcu.set_attitude(roll_angle=5,duration=5)
    time.sleep(3)
    mcu.land()
    mcu.disarm()
    mcu.exit()

run_mcu()

print("Completed")