from swarmlib import Drone, DroneGUI
import threading

def gui_display():
    gui = DroneGUI(D1.vehicle)
    gui.start_gui()
    
print("Connecting to Drone1")
D1 = Drone('tcp:127.0.0.1:5762')
print("Drone1 connected")
gui_display = threading.Thread(target=gui_display)
gui_display.start()
D1.control_with_keyboard()