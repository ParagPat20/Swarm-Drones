from dronekit import mavutil
import time
import socket
import threading

def send_local_ned_velocity(vehicle,velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    print('\n')
    print('{} - Calling function send_local_ned_velocity(Vx={}, Vy={}, Vz={}, Duration={})'.format(time.ctime(), velocity_x, velocity_y, velocity_z, duration))
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    
def send_data(vehicle,ip,port):
    """
    Continuously send data to the Arduino.
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))  # Bind to any available port
    sock.connect((ip, port))
    data_thread = threading.Thread(target=send_data, args=(vehicle))
    data_thread.start()

    while True:
        try:
            # Connect the socket to the Arduino
            sock.connect((ip, port))

            # Get the servo outputs from the vehicle vehicle
            servo_data = {
                'ch1out': vehicle.raw_servo.ch1out,
                'ch2out': vehicle.raw_servo.ch2out,
                'ch3out': vehicle.raw_servo.ch3out,
                'ch4out': vehicle.raw_servo.ch4out
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
