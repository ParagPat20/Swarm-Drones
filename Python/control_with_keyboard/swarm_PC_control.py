import socket
import threading
import tkinter as tk
from tkinter import ttk
import json
import keyboard
from ttkthemes import ThemedStyle

# Initialize P and C dictionaries for two drones
P = {
    0: {'Batt': 0, 'Groundspeed': 0, 'ARM': 0, 'GPS': 0, 'Altitude': 0, 'MODE': None, 'VelocityX': 0, 'VelocityY': 0, 'VelocityZ': 0},
    1: {'Batt': 0, 'Groundspeed': 0, 'ARM': 0, 'GPS': 0, 'Altitude': 0, 'MODE': None, 'VelocityX': 0, 'VelocityY': 0, 'VelocityZ': 0}
}

C = {
    0: {'vx': 0, 'vy': 0, 'vz': 0, 'Arming': 0, 'Mode': 'GUIDED', 'Takeoff': 0},
    1: {'vx': 0, 'vy': 0, 'vz': 0, 'Arming': 0, 'Mode': 'GUIDED', 'Takeoff': 0},
    'drone': None
}

# Create a global variable to keep track of the GUI window
root = tk.Tk()
root.title("Drone Controller")
root.configure(bg="#DAEFFD")
style = ThemedStyle(root)
style.set_theme("itft1")

control_var = tk.IntVar()

def set_control(drone_id):
    control_var.set(drone_id)
    C['drone'] = drone_id

# Create frames to hold labels
frame_labels = [[ttk.Frame(root, relief="solid", padding=10) for _ in range(3)] for _ in range(2)]
for i in range(2):
    for j in range(3):
        frame_labels[i][j].grid(row=i, column=j)

# Create a dictionary to store labels for P dictionary
p_labels = {0: {}, 1: {}}
for i, (key, value) in enumerate(P[0].items()):
    p_label = ttk.Label(frame_labels[0][0], text=f'D1 P: {key}:     ')
    p_label.config(font=("Helvetica", 14))  # Big Font
    p_label.grid(row=i, column=0, sticky="w")
    
    p_value = ttk.Label(frame_labels[0][0], text=str(value), justify="left")
    p_value.config(font=("Helvetica", 14))  # Big Font
    p_value.grid(row=i, column=1, sticky="w")
    
    p_labels[0][key] = p_value

for i, (key, value) in enumerate(P[1].items()):
    p_label = ttk.Label(frame_labels[1][0], text=f'D2 P: {key}:     ')
    p_label.config(font=("Helvetica", 14))  # Big Font
    p_label.grid(row=i, column=0, sticky="w")
    
    p_value = ttk.Label(frame_labels[1][0], text=str(value), justify="left")
    p_value.config(font=("Helvetica", 14))  # Big Font
    p_value.grid(row=i, column=1, sticky="w")
    
    p_labels[1][key] = p_value

# Create a dictionary to store labels for C dictionary
c_labels = {0: {}, 1: {}}
for i, (key, value) in enumerate(C[0].items()):
    c_label = ttk.Label(frame_labels[0][2], text=f'D1 C: {key}:     ')
    c_label.config(font=("Helvetica", 14))  # Big Font
    c_label.grid(row=i, column=0, sticky="w")
    
    c_value = ttk.Label(frame_labels[0][2], text=str(value), justify="left")
    c_value.config(font=("Helvetica", 14))  # Big Font
    c_value.grid(row=i, column=1, sticky="w")
    
    c_labels[0][key] = c_value

for i, (key, value) in enumerate(C[1].items()):
    c_label = ttk.Label(frame_labels[1][2], text=f'D2 C: {key}:     ')
    c_label.config(font=("Helvetica", 14))  # Big Font
    c_label.grid(row=i, column=0, sticky="w")
    
    c_value = ttk.Label(frame_labels[1][2], text=str(value), justify="left")
    c_value.config(font=("Helvetica", 14))  # Big Font
    c_value.grid(row=i, column=1, sticky="w")
    
    c_labels[1][key] = c_value


# Create buttons for control selection at the bottom
control_button1 = ttk.Button(root, text="Drone 1", command=lambda: set_control(0))
control_button2 = ttk.Button(root, text="Drone 2", command=lambda: set_control(1))
control_button3 = ttk.Button(root, text="Both", command=lambda: set_control(-1))


control_button1.grid(row=2, column=0, padx=10, pady=10, sticky="w")
control_button2.grid(row=2, column=1, padx=10, pady=10, sticky="w")
control_button3.grid(row=2, column=2, padx=10, pady=10, sticky="w")

# Create a label to display the currently controlled drone
controlled_drone_label = ttk.Label(root, text="Controlled Drone: None")
controlled_drone_label.config(font=("Helvetica", 14))
controlled_drone_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")

def update_controlled_drone_label():
    drone_id = control_var.get()
    if drone_id == -1:
        controlled_drone_label.config(text="Controlled Drone: Both")
    elif drone_id == 0:
        controlled_drone_label.config(text="Controlled Drone: Drone 1")
    elif drone_id == 1:
        controlled_drone_label.config(text="Controlled Drone: Drone 2")
    else:
        controlled_drone_label.config(text="Controlled Drone: None")
    root.after(100, update_controlled_drone_label)

update_controlled_drone_label()


def update_gui(drone_id):
    # Update the values of P dictionary labels
    for key, value in P[drone_id].items():
        p_labels[drone_id][key].config(text=str(value))

    # Update the values of C dictionary labels
    for key, value in C[drone_id].items():
        c_labels[drone_id][key].config(text=str(value))

    root.after(100, update_gui, drone_id)

update_gui(0)
update_gui(1)

def handle_client(client_socket):
    global P, C
    while True:
        try:
            # Receive P dictionary values for the current drone
            p_str = client_socket.recv(1024).decode()
            P = eval(p_str)  # Convert the received string back to a dictionary
            set_control(drone_id)
            # Send C dictionary values for the selected drone(s)
            c_str = str(C)
            client_socket.send(c_str.encode())
            controller(drone_id)
            print(drone_id)

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
    MAX_VELOCITY = 1
    if keyboard.is_pressed('w'):
        C[drone_id]['vx'] = MAX_VELOCITY  # Move forward
        print(f'Drone {drone_id}: Forward')
    elif keyboard.is_pressed('s'):
        C[drone_id]['vx'] = -MAX_VELOCITY  # Move backward
        print(f'Drone {drone_id}: Backward')
    else:
        C[drone_id]['vx'] = 0

    if keyboard.is_pressed('a'):
        C[drone_id]['vy'] = -MAX_VELOCITY  # Move left
        print(f'Drone {drone_id}: Left')
    elif keyboard.is_pressed('d'):
        C[drone_id]['vy'] = MAX_VELOCITY  # Move right
        print(f'Drone {drone_id}: Right')
    else:
        C[drone_id]['vy'] = 0

    if keyboard.is_pressed('u'):
        C[drone_id]['vz'] = -MAX_VELOCITY  # Increase altitude
        print(f'Drone {drone_id}: Increase Altitude')
    elif keyboard.is_pressed('j'):
        C[drone_id]['vz'] = MAX_VELOCITY  # Decrease altitude
        print(f'Drone {drone_id}: Decrease Altitude')
    else:
        C[drone_id]['vz'] = 0

    if keyboard.is_pressed('m') and P[drone_id]['ARM'] == 0:
        C[drone_id]['Arming'] = 1
    else:
        C[drone_id]['Arming'] = 0

    if keyboard.is_pressed('n') and P[drone_id]['ARM'] == 1 and P[drone_id]['Altitude'] < 1:
        C[drone_id]['Takeoff'] = 1
    else:
        C[drone_id]['Takeoff'] = 0

    if keyboard.is_pressed('q') and P[drone_id]['ARM'] == 1:
        C[drone_id]['Arming'] = 0

    if keyboard.is_pressed('l'):
        C[drone_id]['Mode'] = 'LAND'
    if keyboard.is_pressed('g'):
        C[drone_id]['Mode'] = 'GUIDED'
    if keyboard.is_pressed('p'):
        C[drone_id]['Mode'] = 'STABILIZE'

    if keyboard.is_pressed('h'):
        C[drone_id]['Mode'] = 'AUTOTUNE'
    
    if keyboard.is_pressed('r'):
        C[drone_id]['Mode'] = 'RTL'

def PC_SERVER_start(drone_id):
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

        # Start a new thread to handle client communication
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))  # Wrap client_socket in a tuple
        client_thread.start()

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
