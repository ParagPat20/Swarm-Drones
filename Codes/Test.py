from dronekit import connect
from my_vehicle import MyVehicle  # assuming the MyVehicle class is defined in a file named my_vehicle.py
import argparse
import threading
import socket
import time

ip = "192.168.4.2"  # Replace with your Arduino's IP address
port = 8888  # Replace with the port your Arduino is listening on

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))  # Bind to any available port

# Connect the socket to the Arduino
sock.connect((ip, port))

# Connect to the Vehicles
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Control Copters and send commands in GUIDED mode')
    parser.add_argument('--connect1', help="MCU connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--connect2', help="Client connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()

    connection_string1 = args.connect1
    connection_string2 = args.connect2
    sitl1 = None
    sitl2 = None

    # Start SITL if no connection string is specified for MCU
    if not connection_string1:
        import dronekit_sitl
        sitl1 = dronekit_sitl.start_default()
        connection_string1 = sitl1.connection_string()

    # Start SITL if no connection string is specified for Client
    if not connection_string2:
        import dronekit_sitl
        sitl2 = dronekit_sitl.start_default()
        connection_string2 = sitl2.connection_string()

    # Connect to the Vehicles
    print('Connecting to MCU on: %s' % connection_string1)
    mcu = connect(connection_string1, wait_ready=True, vehicle_class=MyVehicle)

    print('Connecting to Client on: %s' % connection_string2)
    client = connect(connection_string2, wait_ready=True, vehicle_class=MyVehicle)

def send_data(vehicle):
    """
    Continuously send data to the Arduino.
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))  # Bind to any available port

    while True:
        try:
            # Connect the socket to the Arduino
            sock.connect((ip, port))

            # Get the servo outputs from the client vehicle
            servo_data = {
                'ch1out': client.raw_servo.ch1out,
                'ch2out': client.raw_servo.ch2out,
                'ch3out': client.raw_servo.ch3out,
                'ch4out': client.raw_servo.ch4out
            }

            # Combine the servo outputs into a single string
            data = ",".join(str(value) for value in servo_data.values())

            # Send the data to the Arduino
            sock.sendto(data.encode(), (ip, port))

        except Exception as e:
            print("Error sending data:", str(e))

        # Sleep for a short time before sending the next data point
        time.sleep(0.1)

    # Close the socket
    sock.close()

data_thread = threading.Thread(target=send_data, args=(client,))
data_thread.start()
# Arm and Takeoff the vehicles
mcu.armed = True
client.armed = True


# Close vehicle objects before exiting the script
#mcu.close()
client.close()
