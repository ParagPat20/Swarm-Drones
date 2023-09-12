from swarmlib import Drone, DroneGUI
import threading

print("Connecting to Drone1")
D1 = Drone('COM4')
# D1 = Drone('0.0.0.0:14550')
# D1 = Drone('tcp:127.0.0.1:5762')
print("Drone1 connected")
def gui_displayd1():
    gui = DroneGUI(D1.vehicle)
    gui.start_gui()
gui_displayd1 = threading.Thread(target=gui_displayd1)
gui_displayd1.start()
D1.control_with_keyboard()
