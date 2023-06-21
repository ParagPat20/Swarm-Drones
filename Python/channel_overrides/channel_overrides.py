from __future__ import print_function
from dronekit import connect, VehicleMode
import keyboard
import time

# Connect to the Vehicle
vehicle = connect('COM17', wait_ready=True)

# Get all original channel values (before override)
print("Channel values from RC Tx:", vehicle.channels)
vehicle.mode = VehicleMode("STABILIZE")

# Override channels
print("\nChannel overrides: %s" % vehicle.channels.overrides)


channel_values = [1000, 1000, 1000, 1000]  # Initial throttle values for channels 1, 2, 3, 4

print("Set throttle overrides for channels 1, 2, 3, 4 (dictionary syntax)")
vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2], '4': channel_values[3]}
print("Channel overrides: %s" % vehicle.channels.overrides)

print("Press 'w' to increase throttle by 100 for channels 1, 2, 3, 4")
print("Press 's' to decrease throttle by 100 for channels 1, 2, 3, 4")
print("Press 'q' to quit")

last_w_press_time = 0
last_s_press_time = 0
last_a_press_time = 0
delay = 0.2  # Adjust the delay time as needed (in seconds)

# Continuously check for key input
while True:
    if keyboard.is_pressed('a'):
        current_time = time.time()
        if current_time - last_a_press_time >= delay:
            vehicle.armed = True
            print("Vehicle Armed")
            last_a_press_time = current_time

    if keyboard.is_pressed('w'):
        current_time = time.time()
        if current_time - last_w_press_time >= delay:

                if channel_values[i] > 1900:
                    channel_values[i] = 1900
                    print("Channel %d: Value Limit +" % (i + 1))
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_w_press_time = current_time
            print("Throttle values: %s" % channel_values)

    elif keyboard.is_pressed('s'):
        current_time = time.time()
        if current_time - last_s_press_time >= delay:
            for i in range(4):
                channel_values[i] -= 100
                if channel_values[i] < 1000:
                    channel_values[i] = 1000
                    print("Channel %d: Value Limit -" % (i + 1))
            vehicle.channels.overrides = {'1': channel_values[0], '2': channel_values[1], '3': channel_values[2],
                                          '4': channel_values[3]}
            last_s_press_time = current_time
            print("Throttle values: %s" % channel_values)

    elif keyboard.is_pressed('q'):
        print("Vehicle Disarmed")
        vehicle.armed = False

    elif keyboard.is_pressed('r'):
        print("Vehicle Disarmed")
        vehicle.armed = False
        break
print("Completed")
