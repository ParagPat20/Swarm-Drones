from __future__ import print_function
from dronekit import connect, VehicleMode
import keyboard
import time

# Connect to the Vehicle
vehicle = connect('COM4')

# Get all original channel values (before override)
print("Channel values from RC Tx:", vehicle.channels)

# Override channels
print("\nChannel overrides: %s" % vehicle.channels.overrides)

channel_values = [1500, 1500, 1000, 1500, 1000]  # Initial channel values for throttle, roll, yaw, pitch

print("Set throttle, roll, yaw, and pitch overrides (dictionary syntax)")
vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2], '4': channel_values[3], '5': channel_values[4]}
print("Channel overrides: %s" % vehicle.channels.overrides)

print("Press 'w' to increase throttle by 100")
print("Press 's' to decrease throttle by 100")
print("Press 'a' to increase roll by 100")
print("Press 'd' to decrease roll by 100")
print("Press 'q' to increase yaw by 100")
print("Press 'e' to decrease yaw by 100")
print("Press 'z' to increase pitch by 100")
print("Press 'x' to decrease pitch by 100")
print("Press 'r' to disarm the vehicle and exit")

last_w_press_time = 0
last_s_press_time = 0
last_a_press_time = 0
last_d_press_time = 0
last_q_press_time = 0
last_e_press_time = 0
last_z_press_time = 0
last_x_press_time = 0
last_l_press_time = 0
delay = 0.2  # Adjust the delay time as needed (in seconds)

# Continuously check for key input
while True:
    if keyboard.is_pressed('w'):
        current_time = time.time()
        if current_time - last_w_press_time >= delay:
            channel_values[2] += 20  # Increase throttle channel (Ch3) by 20
            if channel_values[2] > 1900:
                channel_values[2] = 1900
                print("Throttle: Value Limit +")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_w_press_time = current_time
            print("Throttle value: %s" % channel_values[2])

    if keyboard.is_pressed('s'):
        current_time = time.time()
        if current_time - last_s_press_time >= delay:
            channel_values[2] -= 20  # Decrease throttle channel (Ch3) by 20
            if channel_values[2] < 1000:
                channel_values[2] = 1000
                print("Throttle: Value Limit -")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_s_press_time = current_time
            print("Throttle value: %s" % channel_values[2])

    if keyboard.is_pressed('a'):
        current_time = time.time()
        if current_time - last_a_press_time >= delay:
            channel_values[0] += 30  # Increase roll channel (Ch1) by 100
            if channel_values[0] > 1900:
                channel_values[0] = 1900
                print("Roll: Value Limit +")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_a_press_time = current_time
            print("Roll value: %s" % channel_values[0])

    if keyboard.is_pressed('d'):
        current_time = time.time()
        if current_time - last_d_press_time >= delay:
            channel_values[0] -= 30  # Decrease roll channel (Ch1) by 100
            if channel_values[0] < 1000:
                channel_values[0] = 1000
                print("Roll: Value Limit -")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_d_press_time = current_time
            print("Roll value: %s" % channel_values[0])

    if keyboard.is_pressed('q'):
        current_time = time.time()
        if current_time - last_q_press_time >= delay:
            channel_values[3] += 30  # Increase yaw channel (Ch4) by 100
            if channel_values[3] > 1900:
                channel_values[3] = 1900
                print("Yaw: Value Limit +")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_q_press_time = current_time
            print("Yaw value: %s" % channel_values[3])

    if keyboard.is_pressed('e'):
        current_time = time.time()
        if current_time - last_e_press_time >= delay:
            channel_values[3] -= 30  # Decrease yaw channel (Ch4) by 100
            if channel_values[3] < 1000:
                channel_values[3] = 1000
                print("Yaw: Value Limit -")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_e_press_time = current_time
            print("Yaw value: %s" % channel_values[3])

    if keyboard.is_pressed('z'):
        current_time = time.time()
        if current_time - last_z_press_time >= delay:
            channel_values[1] += 30  # Increase pitch channel (Ch2) by 100
            if channel_values[1] > 1900:
                channel_values[1] = 1900
                print("Pitch: Value Limit +")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_z_press_time = current_time
            print("Pitch value: %s" % channel_values[1])

    if keyboard.is_pressed('x'):
        current_time = time.time()
        if current_time - last_x_press_time >= delay:
            channel_values[1] -= 30  # Decrease pitch channel (Ch2) by 100
            if channel_values[1] < 1000:
                channel_values[1] = 1000
                print("Pitch: Value Limit -")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_x_press_time = current_time
            print("Pitch value: %s" % channel_values[1])

    if keyboard.is_pressed('r'):
        print("Vehicle Disarmed")
        channel_values[4] = 1000
        vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2], '4': channel_values[3], '5': channel_values[4]}

    if keyboard.is_pressed('l'):
        current_time = time.time()
        if current_time - last_l_press_time >= delay:
            channel_values[4] = 2000
            print("Vehicle landing")
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2], '4': channel_values[3], '5': channel_values[4]}
            last_a_press_time = current_time
    
    if keyboard.is_pressed('esc'):
        print("Can not control")
        break

print("Completed")