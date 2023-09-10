from swarmlib import Drone, DroneGUI
import threading
    
print("Connecting to Drone1")
# D1 = Drone('0.0.0.0:14550')
D1 = Drone('tcp:127.0.0.1:5762')
D2 = Drone('tcp:127.0.0.1:5772')
D3 = Drone('tcp:127.0.0.1:5782')

def d1control():
    D1.control_with_keyboard()
    print("Drone1 connected")
def gui_displayd1():
    gui = DroneGUI(D1.vehicle)
    gui.start_gui()

def d2control():
    D2.control_with_keyboard()
    print("Drone2 connected")
def gui_displayd2():
    gui = DroneGUI(D2.vehicle)
    gui.start_gui()

def d3control():
    D3.control_with_keyboard()
    print("Drone1 connected")
def gui_displayd3():
    gui = DroneGUI(D3.vehicle)
    gui.start_gui()

gui_displayd1 = threading.Thread(target=gui_displayd1)
gui_displayd1.start()
gui_displayd2 = threading.Thread(target=gui_displayd2)
gui_displayd2.start()
gui_displayd3 = threading.Thread(target=gui_displayd3)
gui_displayd3.start()
d1=threading.Thread(target=d1control)
d2=threading.Thread(target=d2control)
d3=threading.Thread(target=d3control)
d1.start()
d2.start()
d3.start()
