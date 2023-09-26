import socket
import threading
import tkinter as tk
from tkinter import ttk
import keyboard
from ttkthemes import ThemedStyle
import time
import pickle

# Create a dictionary to store the drone control values
C = {
    'Drone': 0,
    'vx': 0, 
    'vy': 0, 
    'vz': 0, 
    'Arming': 0, 
    'Mode': 'GUIDED',
    'Takeoff': 0
    }

P = {
    'MCU':{
        'Batt' : 0,
        'Groundspeed': 0,
        'ARM': 0,
        'GPS': 0,
        'Altitude': 0,
        'MODE': None,
        'VelocityX': 0,
        'VelocityY': 0,
        'VelocityZ': 0
        },
    'Drone':{
        'Batt' : 0,
        'Groundspeed': 0,
        'ARM': 0,
        'GPS': 0,
        'Altitude': 0,
        'MODE': None,
        'VelocityX': 0,
        'VelocityY': 0,
        'VelocityZ': 0
    }
    }

# Create a global variable to keep track of the GUI window
root = tk.Tk()
root.title("Drone Controller")
style = ThemedStyle(root)
style.set_theme("kroc")

control_var = tk.IntVar()

def set_control(drone_id):
    control_var.set(drone_id)
    C['Drone'] = drone_id

# Create frames to hold labels for P dictionary
frame_labels_P = [[ttk.Frame(root, relief="solid", padding=10) for _ in range(3)] for _ in range(2)]
for i in range(2):
    for j in range(3):
        frame_labels_P[i][j].grid(row=i, column=j)  # Adjust column position

# Create a dictionary to store labels for P dictionary
p_labels = {}
for i, (key, value) in enumerate(P['MCU'].items()):  # You can choose 'MCU' or 'Drone'
    p_label = ttk.Label(frame_labels_P[0][2], text=f'MCU {key  }:     ')
    p_label.config(font=("Helvetica", 14))  # Big Font
    p_label.grid(row=i, column=0, sticky="w")
    
    p_value = ttk.Label(frame_labels_P[0][2], text=str(value), justify="left")
    p_value.config(font=("Helvetica", 14))  # Big Font
    p_value.grid(row=i, column=1, sticky="w")
    
    p_labels[key] = p_value

# Create frames to hold labels for P dictionary
frame_labels_P1 = [[ttk.Frame(root, relief="solid", padding=10) for _ in range(3)] for _ in range(2)]
for i in range(2):
    for j in range(3):
        frame_labels_P1[i][j].grid(row=i+1, column=j)  # Adjust column position

p_labels1 = {}
for i, (key, value) in enumerate(P['Drone'].items()):  # You can choose 'MCU' or 'Drone'
    p_label1 = ttk.Label(frame_labels_P1[0][2], text=f'CD {key}  :     ')
    p_label1.config(font=("Helvetica", 14))  # Big Font
    p_label1.grid(row=i, column=0, sticky="w")
    
    p_value1 = ttk.Label(frame_labels_P1[0][2], text=str(value), justify="left")
    p_value1.config(font=("Helvetica", 14))  # Big Font
    p_value1.grid(row=i, column=1, sticky="w")
    
    p_labels1[key] = p_value1

# Create frames to hold labels
frame_labels = [[ttk.Frame(root, relief="solid", padding=10) for _ in range(3)] for _ in range(2)]
for i in range(2):
    for j in range(3):
        frame_labels[i][j].grid(row=i, column=j+3)

# Create a dictionary to store labels for C dictionary
c_labels = {}
for i, (key, value) in enumerate(C.items()):
    c_label = ttk.Label(frame_labels[0][2], text=f'{key}:     ')
    c_label.config(font=("Helvetica", 14))  # Big Font
    c_label.grid(row=i, column=0, sticky="w")
    
    c_value = ttk.Label(frame_labels[0][2], text=str(value), justify="left")
    c_value.config(font=("Helvetica", 14))  # Big Font
    c_value.grid(row=i, column=1, sticky="w")
    
    c_labels[key] = c_value


# Create buttons for control selection at the bottom
control_button1 = ttk.Button(root, text="MCU", command=lambda: set_control(1))
control_button2 = ttk.Button(root, text="CD", command=lambda: set_control(2))
control_button3 = ttk.Button(root, text="Both", command=lambda: set_control(-1))

control_button1.grid(row=4, column=2, padx=10, pady=10, sticky="w")
control_button2.grid(row=5, column=2, padx=10, pady=10, sticky="w")
control_button3.grid(row=4, column=3, padx=10, pady=10, sticky="w")

# Create a label to display the currently controlled drone
controlled_drone_label = ttk.Label(root, text="Controlled Drone: None")
controlled_drone_label.config(font=("Helvetica", 14))
controlled_drone_label.grid(row=6, column=2, columnspan=3, padx=10, pady=10, sticky="w")

def update_controlled_drone_label():
    global P,C
    drone_id = control_var.get()
    if drone_id == -1:
        controlled_drone_label.config(text="Controlled Drone: Both")
    elif drone_id == 1:
        controlled_drone_label.config(text="Controlled Drone: MCU")
    elif drone_id == 2:
        controlled_drone_label.config(text="Controlled Drone: CD")
    else:
        controlled_drone_label.config(text="Controlled Drone: None")
    root.after(100, update_controlled_drone_label)

update_controlled_drone_label()

def update_gui():
    global P, C
    # Update the values of MCU dictionary labels
    for key, value in P['MCU'].items():
        p_labels[key].config(text=str(value))
    
    # Update the values of Drone dictionary labels
    for key, value in P['Drone'].items():
        p_labels1[key].config(text=str(value))
    
    # Update the values of C dictionary labels
    for key, value in C.items():
        c_labels[key].config(text=str(value))

    root.after(10, update_gui)

update_gui()

def handle_client(drone_id, client_socket):
    global C,P
    while True:
        try:
            # Send C dictionary values for the selected drone(s) using pickle
            c_pickle = pickle.dumps(C)
            client_socket.send(c_pickle)
            controller(drone_id)
            p_pickle = client_socket.recv(1024)
            if not p_pickle:
                break
            P = pickle.loads(p_pickle)
            time.sleep(0.5)
        except KeyboardInterrupt:
            print(f"Server for drone {drone_id} stopped.")
            break
        except Exception as e:
            print(f"Error handling client for drone {drone_id}: {str(e)}")
            break
        if keyboard.is_pressed('esc'):
            print(f"Client for drone {drone_id} closed.")
            break

def controller(drone_id):
    global P,C
    MAX_VELOCITY = 0.5
    if keyboard.is_pressed('w'):
        C['vx'] = MAX_VELOCITY  # Move forward
        print(f'Drone {drone_id}: Forward')
    elif keyboard.is_pressed('s'):
        C['vx'] = -MAX_VELOCITY  # Move backward
        print(f'Drone {drone_id}: Backward')
    else:
        C['vx'] = 0

    if keyboard.is_pressed('a'):
        C['vy'] = -MAX_VELOCITY  # Move left
        print(f'Drone {drone_id}: Left')
    elif keyboard.is_pressed('d'):
        C['vy'] = MAX_VELOCITY  # Move right
        print(f'Drone {drone_id}: Right')
    else:
        C['vy'] = 0

    if keyboard.is_pressed('u'):
        C['vz'] = -MAX_VELOCITY  # Increase altitude
        print(f'Drone {drone_id}: Increase Altitude')
    elif keyboard.is_pressed('j'):
        C['vz'] = MAX_VELOCITY  # Decrease altitude
        print(f'Drone {drone_id}: Decrease Altitude')
    else:
        C['vz'] = 0

    if keyboard.is_pressed('m'):
        C['Arming'] = 1
    else:
        C['Arming'] = 0

    if keyboard.is_pressed('n'):
        C['Takeoff'] = 1
    else:
        C['Takeoff'] = 0

    if keyboard.is_pressed('q') and P['ARM'] == 1:
        C['Arming'] = 0

    if keyboard.is_pressed('l'):
        C['Mode'] = 'LAND'
    if keyboard.is_pressed('g'):
        C['Mode'] = 'GUIDED'
    if keyboard.is_pressed('p'):
        C['Mode'] = 'POSHOLD'

    if keyboard.is_pressed('h'):
        C['Mode'] = 'AUTOTUNE'
    
    if keyboard.is_pressed('r'):
        C['Mode'] = 'RTL'

def PC_SERVER_start(drone_id):
    global P,C
    # Define server socket parameters
    server_ip = '0.0.0.0'  # Listen on all available network interfaces
    server_port = 12345 + drone_id  # Choose a port for communication

    # Create a socket object and bind it to the server address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen()
    print(f"Server for drone {drone_id} is listening for connections...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to drone {drone_id}: {client_address}")

        handle_client(drone_id, client_socket)
        time.sleep(0.5)
        if keyboard.is_pressed('esc'):
            server_socket.close()
            print(f"Connection to drone {drone_id} closed.")
            break

if __name__ == "__main__":
    for drone_id in range(2):
        # Start the server for each drone in a separate thread
        server_thread = threading.Thread(target=PC_SERVER_start, args=(drone_id,))
        server_thread.daemon = True
        server_thread.start()

    # Start the Tkinter GUI main loop
    root.mainloop()