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
    1: {'vx': 0, 'vy': 0, 'vz': 0, 'Arming': 0, 'Mode': 'GUIDED', 'Takeoff': 0}
}

# Create a global variable to keep track of the GUI window
root = tk.Tk()
root.title("Drone Controller")

style = ThemedStyle(root)
style.set_theme("adapta")

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

# Create battery progress bars and labels for both drones
battery_labels = [ttk.Label(frame_labels[0][1], text="D1 Battery Level:"), ttk.Label(frame_labels[1][1], text="D2 Battery Level:")]
battery_labels[0].config(font=("Helvetica", 14))  # Big Font
battery_labels[1].config(font=("Helvetica", 14))  # Big Font
battery_labels[0].grid(row=0, column=0, sticky="w")
battery_labels[1].grid(row=0, column=0, sticky="w")

battery_bars = [ttk.Progressbar(frame_labels[0][1], length=100, mode="determinate", style="Custom.Horizontal.TProgressbar"),
               ttk.Progressbar(frame_labels[1][1], length=100, mode="determinate", style="Custom.Horizontal.TProgressbar")]

for i in range(2):
    battery_bars[i].grid(row=0, column=1, sticky="w", padx=10)

# Define custom styles for progress bar
style.configure("Custom.Horizontal.TProgressbar", troughcolor="white")
style.configure("Green.Horizontal.TProgressbar", troughcolor="white", background="green")
style.configure("Red.Horizontal.TProgressbar", troughcolor="white", background="red")

# Set the maximum battery level
max_battery_level = 12.8

def map_battery_level(battery_level):
    return (battery_level / max_battery_level) * 100

def update_gui(drone_id):
    # Update the values of P dictionary labels
    for key, value in P[drone_id].items():
        p_labels[drone_id][key].config(text=str(value))

    # Update the values of C dictionary labels
    for key, value in C[drone_id].items():
        c_labels[drone_id][key].config(text=str(value))

    # Update the battery bar
    battery_level = P[drone_id]['Batt']
    battery_percentage = map_battery_level(battery_level)
    battery_bars[drone_id]["value"] = battery_percentage

    if battery_level <= 10.8:
        battery_bars[drone_id]["style"] = "Red.Horizontal.TProgressbar"
    else:
        battery_bars[drone_id]["style"] = "Green.Horizontal.TProgressbar"

    root.after(100, update_gui, drone_id)

update_gui(0)
update_gui(1)

def handle_client(drone_id, client_socket):
    global P, C
    while True:
        try:
            # Receive P dictionary values from the client
            p_str = client_socket.recv(1024).decode()
            P[drone_id] = eval(p_str)  # Convert the received string back to a dictionary

            # Process the received data as needed
            # Example: Print P dictionary
            update_gui(drone_id)
            
            # Send C dictionary values to the client
            c_str = str(C[drone_id])
            client_socket.send(c_str.encode())
            controller(drone_id)
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
        client_thread = threading.Thread(target=handle_client, args=(drone_id, client_socket))
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
