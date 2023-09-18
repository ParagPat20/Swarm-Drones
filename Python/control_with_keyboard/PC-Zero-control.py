import socket
import keyboard
import threading
import time

C = {'vx': 0, 'vy': 0, 'vz': 0, 'Arming': 0, 'Mode': 0, 'Takeoff' : 0}

def handle_client(client_socket):
    while True:
        try:
            # Receive P dictionary values from the client
            p_str = client_socket.recv(1024).decode()
            P = eval(p_str)  # Convert the received string back to a dictionary

            # Process the received data as needed
            # Example: Print P dictionary
            print("Received P:", P)

            # Send C dictionary values to the client
            c_str = str(C)
            client_socket.send(c_str.encode())
            controller()
        except KeyboardInterrupt:
            print("Server stopped.")
            break
        except Exception as e:
            print("Error handling client:", str(e))
            break

def controller():
    MAX_VELOCITY = 0.5
    if keyboard.is_pressed('w'):
        C['vx'] = MAX_VELOCITY  # Move forward
        print('w')
    elif keyboard.is_pressed('s'):
        C['vx'] = -MAX_VELOCITY  # Move backward
        print('s')
    else:
        C['vx'] = 0

    if keyboard.is_pressed('a'):
        C['vy'] = -MAX_VELOCITY  # Move left
        print('a')
    elif keyboard.is_pressed('d'):
        C['vy'] = MAX_VELOCITY  # Move right
        print('d')
    else:
        C['vy'] = 0

    if keyboard.is_pressed('u'):
        C['vz'] = -MAX_VELOCITY  # Increase altitude
        print('u')
    elif keyboard.is_pressed('j'):
        C['vz'] = MAX_VELOCITY  # Decrease altitude
        print('j')
    else:
        C['vz'] = 0

    if keyboard.is_pressed('m'):
        C['Arming'] = 1

    if keyboard.is_pressed('n'):
        C['Takeoff'] = 1
    if keyboard.is_pressed('b'):
        C['Takeoff'] = 0
    if keyboard.is_pressed('q'):
        C['Arming'] = 0
    if keyboard.is_pressed('l'):
        C['Mode'] = 'LAND'
    if keyboard.is_pressed('g'):
        C['Mode'] = 'GUIDED'
    if keyboard.is_pressed('p'):
        C['Mode'] = 'STABILIZE'

def PC_SERVER_start():
    # Define server socket parameters
    server_ip = '0.0.0.0'  # Listen on all available network interfaces
    server_port = 12345  # Choose a port for communication

    # Create a socket object and bind it to the server address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen()
    print("Server is listening for connections...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Connected to:", client_address)

        # Start a new thread to handle client communication
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    # Start the PC server
    PC_SERVER_start()
