import keyboard
import socket
import threading



C = {'Drone':0, 'vx': 0, 'vy': 0, 'vz': 0, 'Arming': 0, 'Mode': 'GUIDED', 'Takeoff': 0, 'mstart': False}
P = {
    1:{'Batt': 0, 'Groundspeed': 0, 'ARM': 0, 'GPS': 0, 'Altitude': 0, 'MODE': None, 'VelocityX': 0, 'VelocityY': 0, 'VelocityZ': 0},
    2:{'Batt': 0, 'Groundspeed': 0, 'ARM': 0, 'GPS': 0, 'Altitude': 0, 'MODE': None, 'VelocityX': 0, 'VelocityY': 0, 'VelocityZ': 0}
}
def controller():
    MAX_VELOCITY = 1
    if keyboard.is_pressed('w'):
        C['vx'] = MAX_VELOCITY  # Move forward
        print(f'Drone  Forward')
    elif keyboard.is_pressed('s'):
        C['vx'] = -MAX_VELOCITY  # Move backward
        print(f'Drone  Backward')
    else:
        C['vx'] = 0

    if keyboard.is_pressed('a'):
        C['vy'] = -MAX_VELOCITY  # Move left
        print(f'Drone  Left')
    elif keyboard.is_pressed('d'):
        C['vy'] = MAX_VELOCITY  # Move right
        print(f'Drone  Right')
    else:
        C['vy'] = 0

    if keyboard.is_pressed('u'):
        C['vz'] = -MAX_VELOCITY  # Increase altitude
        print(f'Drone  Increase Altitude')
    elif keyboard.is_pressed('j'):
        C['vz'] = MAX_VELOCITY  # Decrease altitude
        print(f'Drone  Decrease Altitude')
    else:
        C['vz'] = 0

    if keyboard.is_pressed('m') and P['ARM'] == 0:
        C['Arming'] = 1
    else:
        C['Arming'] = 0

    if keyboard.is_pressed('n') and P['ARM'] == 1 and P['Altitude'] < 1:
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
        C['Mode'] = 'STABILIZE'

    if keyboard.is_pressed('h'):
        C['Mode'] = 'AUTOTUNE'
    
    if keyboard.is_pressed('r'):
        C['Mode'] = 'RTL'

def set_control(drone_id):
    C['Drone'] = drone_id

def init(client_socket,drone_id):
    global P, C
    c_str = str(C)
    client_socket.send(c_str.encode())
    set_control(drone_id = drone_id)
    p_str = client_socket.recv(1024).decode()
    P = eval(p_str)

def PC_Server(drone_id):
    server_ip = '0.0.0.0'
    server_port = 12345 + drone_id

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen()
    print(f"Server for drone {drone_id} is listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to drone {drone_id}: {client_address}")\
        
        client_thread = threading.Thread(target=init, args=(client_socket,drone_id))  # Wrap client_socket in a tuple
        client_thread.start()
for drone_id in range(2):
    # Start the server for each drone in a separate thread
    server_thread = threading.Thread(target=PC_Server, args=(drone_id,))
    server_thread.daemon = True
    server_thread.start()