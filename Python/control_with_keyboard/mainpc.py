import socket
import threading
import keyboard
import time
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

local_host = '192.168.155.122'
remote_host = '192.168.155.122'
mode_port = 12345
ctrl_port = 60003
status_port = [60002, 60004]
Drone_ID = 'D0'

def ClientSendMode(remote_host, cmd_str):
    global mode_port
    # Create a socket object
    client_socket = socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client_socket.connect((remote_host, mode_port))
    except socket.error as error_msg:
        print('{} - Caught exception : {}'.format(time.ctime(), error_msg))
        print('{} - ClientSendMode({}, {}) is not executed!'.format(time.ctime(), remote_host, cmd_str))
        return
    client_socket.send(cmd_str.encode())  # Encode the string as bytes before sending

def ModeControl(remote_host):
    if keyboard.is_pressed('m'):
        ClientSendMode(remote_host, 'ARM')
    if keyboard.is_pressed('n'):
        ClientSendMode(remote_host, 'TakeOff')
    if keyboard.is_pressed('o'):
        ClientSendMode(remote_host, 'takeoff')
    if keyboard.is_pressed('l'):
        ClientSendMode(remote_host, 'LAND')
    if keyboard.is_pressed('b'):
        ClientSendMode(remote_host, 'land_all')
    if keyboard.is_pressed('p'):
        ClientSendMode(remote_host, 'POSHOLD')
    if keyboard.is_pressed('v'):
        ClientSendMode(remote_host, 'square')
    if keyboard.is_pressed('k'):
        ClientSendMode(remote_host, 'line')
    if keyboard.is_pressed('x'):
        ClientSendMode(remote_host, 'tri')
    if keyboard.is_pressed('c'):
        ClientSendMode(remote_host, 'circle')

def ClientRecvStatus(status_port):
    global remote_host
    client_socket = socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client_socket.connect((remote_host, status_port))
    except socket.error as error_msg:
        print('{} - Caught exception : {}'.format(time.ctime(), error_msg))
        print('{} - recvCTRL({}) is not executed!'.format(time.ctime(), remote_host))
    status_bytes = client_socket.recv(1024)  # Receive bytes
    status_str = status_bytes.decode()  # Decode bytes to a string
    status_data = status_str.split(',')

    if len(status_data) == 11:
        b, gs, md, vx, vy, vz, gps, lat, lon, alt, armed = status_data
        return [float(b), float(gs), str(md), str(vx), str(vy), str(vz), int(gps), float(lat), float(lon), float(alt), str(armed)]
    else:
        print('Received invalid status data:', status_data)
        return []  # Handle the case when the received data doesn't match the expected format

def ClientSendCtrl(remote_host):
    global ctrl_port
    # Create a socket object
    client_socket = socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client_socket.connect((remote_host, ctrl_port))
    except socket.error as error_msg:
        print('{} - Caught exception : {}'.format(time.ctime(), error_msg))
        print('{} - ClientSendCtrl({}, {}) is not executed!'.format(time.ctime(), remote_host))
        return
    client_socket.send(ctrl().encode())  # Encode the string as bytes before sending

def ctrl():
    Velocity = 0.5

    if keyboard.is_pressed('w'):
        x = str(Velocity)
    elif keyboard.is_pressed('s'):
        x = str(-Velocity)
    else:
        x = '0'

    if keyboard.is_pressed('a'):
        y = str(Velocity)
    elif keyboard.is_pressed('d'):
        y = str(-Velocity)
    else:
        y = '0'

    if keyboard.is_pressed('u'):
        z = str(-Velocity)
    elif keyboard.is_pressed('j'):
        z = str(Velocity)
    else:
        z = '0'

    ctrl_str = x + ',' + y + ',' + z

    return ctrl_str

def update_gui_label(status_port, label):
    while True:
        try:
            status_data = ClientRecvStatus(status_port)
            if status_data:
                formatted_status = (
                    f"Battery Voltage: {status_data[0]}\n"
                    f"Groundspeed: {status_data[1]}\n"
                    f"Mode: {status_data[2]}\n"
                    f"Velocity X: {status_data[3]}\n"
                    f"Velocity Y: {status_data[4]}\n"
                    f"Velocity Z: {status_data[5]}\n"
                    f"GPS Fix Type: {status_data[6]}\n"
                    f"Latitude: {status_data[7]}\n"
                    f"Longitude: {status_data[8]}\n"
                    f"Altitude: {status_data[9]}\n"
                    f"Armed: {status_data[10]}"
                )
                label.config(text=formatted_status)
        except Exception as e:
            print(f"Error in update_gui_label: {str(e)}")

def control_drone(remote_host):
    while True:
        ModeControl(remote_host)
        if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('a') or keyboard.is_pressed('d') or keyboard.is_pressed('u') or keyboard.is_pressed('j'):
            ClientSendCtrl(remote_host)
        time.sleep(1)

def change_drone_id(new_id):
    global Drone_ID
    global remote_host
    Drone_ID = new_id
    print(f"Drone_ID changed to {new_id}")
    ClientSendMode(remote_host,Drone_ID)

def update_gui_label_thread(status_port, label):
    update_gui_thread = threading.Thread(target=update_gui_label, args=(status_port, label))
    update_gui_thread.daemon = True
    update_gui_thread.start()

# Create the main window using ThemedTk for themed widgets
root = ThemedTk(theme="plastik")  # Change the theme to your preferred one
root.title("Drone Status")

# Create a frame for the drone status labels
status_frame = ttk.Frame(root)
status_frame.pack(padx=20, pady=20)

# Create a label to display the status for each drone
status_label = ttk.Label(status_frame, text="", font=("Helvetica", 12))
status_label.grid(row=0, column=0, padx=10)

status_label_2 = ttk.Label(status_frame, text="", font=("Helvetica", 12))
status_label_2.grid(row=0, column=1, padx=10)

status_label_3 = ttk.Label(status_frame, text="", font=("Helvetica", 12))
status_label_3.grid(row=0, column=2, padx=10)

status_label_4 = ttk.Label(status_frame, text="", font=("Helvetica", 12))
status_label_4.grid(row=0, column=3, padx=10)

info_label = ttk.Label(root, text="Press 'm' for ARM, 'n' for TakeOff, 'o' for takeoff, etc.", font=("Helvetica", 10))
info_label.pack(pady=10)

# Create a frame for the drone selection buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

# Create buttons for selecting drones
button_mcu = ttk.Button(button_frame, text="MCU", command=lambda: change_drone_id('MCU'))
button_cd1 = ttk.Button(button_frame, text="CD1", command=lambda: change_drone_id('CD1'))
button_cd2 = ttk.Button(button_frame, text="CD2", command=lambda: change_drone_id('CD2'))
button_cd3 = ttk.Button(button_frame, text="CD3", command=lambda: change_drone_id('CD3'))

# Pack the buttons
button_mcu.grid(row=0, column=0, padx=10)
button_cd1.grid(row=0, column=1, padx=10)
button_cd2.grid(row=0, column=2, padx=10)
button_cd3.grid(row=0, column=3, padx=10)

info_text = (
    "Key-Action Mappings:\n"
    "'m' for ARM\n"
    "'o' for TakeOff\n"
    "'n' for TakeOff individually\n"
    "'b' for land_all\n"
    "'p' for POSHOLD\n"
    "'v' for square\n"
    "'k' for line\n"
    "'x' for tri\n"
    "'c' for circle\n\n\n"
    "'w' for forward\n"
    "'s' for backward\n"
    "'a' for left\n"
    "'d' for right\n"
    "'u' for up\n"
    "'j' for down"
)
info_label.config(text=info_text)

# Start threads to update the GUI labels
update_gui_label_thread(status_port[0], status_label)
# update_gui_label_thread(status_port[1], status_label_2)

# Start a thread for controlling the drone
control_thread = threading.Thread(target=control_drone, args=(remote_host,))
control_thread.daemon = True
control_thread.start()

# Start the tkinter main loop
root.mainloop()