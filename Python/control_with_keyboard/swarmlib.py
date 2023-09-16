from __future__ import print_function
from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time
import keyboard

class Drone:
    def __init__(self, connection_string):
        self.vehicle = connect(connection_string)

    def send_ned_velocity(self, velocity_x, velocity_y, velocity_z, duration):

        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
            0b0000111111000111, # type_mask (only speeds enabled)
            0, 0, 0, # x, y, z positions (not used)
            velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
            0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        # send command to vehicle on 1 Hz cycle
        for x in range(0,duration):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
            if keyboard.is_pressed('l'):
                self.land()
                break

    def takeoff(self, aTargetAltitude):
        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude)
        while True:
            current_altitude = self.vehicle.location.global_relative_frame.alt
            if current_altitude is not None:
                print(" Altitude: ", current_altitude)
                if current_altitude >= aTargetAltitude * 0.9:
                    print("Reached target altitude")
                    break
                if keyboard.is_pressed('l'):
                    self.land()
                    break
            else:
                print("Waiting for altitude information...")
            time.sleep(1)

    def arm(self,mode='GUIDED'):
        print("Arming motors")
        self.vehicle.mode = VehicleMode(mode)
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print("Waiting for arming...")
            self.vehicle.armed = True
            time.sleep(1)
            if keyboard.is_pressed('q'):
                break
        print("Vehicle Armed")

    def disarm(self):
        print("Disarming motors")
        self.vehicle.armed = False

        while self.vehicle.armed:
            print("Waiting for disarming...")
            self.vehicle.armed = False
            time.sleep(1)
            if keyboard.is_pressed('q'):
                break
        print("Vehicle Disarmed")

    def land(self):
        self.vehicle.mode = VehicleMode("LAND")
        print("Landing")

    def exit(self):
        self.vehicle.close()
        print("Completed")
    
    def control_with_keyboard(self):
        # Initialize velocity components
        vel_x = 0
        vel_y = 0
        vel_z = 0

        # Define the maximum velocity (m/s)
        MAX_VELOCITY = 0.7

        print("Use arrow keys to control the drone. Press 'Esc' to exit.")

        while True:

            if keyboard.is_pressed('m'):
                self.arm()

            if keyboard.is_pressed('n'):
                self.takeoff(1)

            # Check for key presses to control the drone
            if keyboard.is_pressed('w'):
                vel_x = MAX_VELOCITY  # Move forward
                print('w')
            elif keyboard.is_pressed('s'):
                vel_x = -MAX_VELOCITY  # Move backward
                print('s')
            else:
                vel_x = 0

            if keyboard.is_pressed('a'):
                vel_y = -MAX_VELOCITY  # Move left
                print('a')
            elif keyboard.is_pressed('d'):
                vel_y = MAX_VELOCITY  # Move right
                print('d')
            else:
                vel_y = 0

            if keyboard.is_pressed('u'):
                vel_z = -MAX_VELOCITY  # Increase altitude
                print('u')
            elif keyboard.is_pressed('j'):
                vel_z = MAX_VELOCITY  # Decrease altitude
                print('j')
            else:
                vel_z = 0

            # Send NED velocity commands
            self.send_ned_velocity(vel_x, vel_y, vel_z, 1)

            if keyboard.is_pressed('l'):
                self.land()

            if keyboard.is_pressed('q'):
                self.disarm()

            if keyboard.is_pressed('p'):
                self.vehicle.mode = VehicleMode('POSHOLD')
            
            if keyboard.is_pressed('g'):
                self.vehicle.mode = VehicleMode('GUIDED')

            if keyboard.is_pressed('k'):
                self.vehicle.mode = VehicleMode('GUIDED')
                time.sleep(1)
                self.arm()
                time.sleep(2)
                self.takeoff(2)
                self.send_ned_velocity(0,0,0,1)
                time.sleep(1)

                print("Forward")
                self.send_ned_velocity(0.7,0,0,8)
                print("Right")
                self.send_ned_velocity(0,0.7,0,8)
                print("Backward")
                self.send_ned_velocity(-0.7,0,0,8)
                print("Left")
                self.send_ned_velocity(0,-0.7,0,8)
                self.land()
            # Exit the loop if the 'Esc' key is pressed
            if keyboard.is_pressed('esc'):
                self.send_ned_velocity(0, 0, 0, 1)  # Stop the drone before exiting
                print("Can not control the drone anymore")
                break

import tkinter as tk

class DroneGUI:
    def __init__(self, vehicle):
        self.vehicle = vehicle

        # Create the main GUI window
        self.root = tk.Tk()
        self.root.title("Drone Status")

        # Labels to display connection status and connection string
        self.connection_label = tk.Label(self.root, text="Connected")
        self.connection_label.pack()
        self.connection_string_label = tk.Label(self.root, text=f"Connection String: {self.vehicle._master.address}")
        self.connection_string_label.pack()

        # Labels to display online/offline status
        self.online_status_label = tk.Label(self.root, text="Online")
        self.online_status_label.pack()

        # Labels to display current altitude, velocities, and additional details
        self.altitude_label = tk.Label(self.root, text="Altitude: ")
        self.altitude_label.pack()
        self.velocity_x_label = tk.Label(self.root, text="Velocity X: ")
        self.velocity_x_label.pack()
        self.velocity_y_label = tk.Label(self.root, text="Velocity Y: ")
        self.velocity_y_label.pack()
        self.velocity_z_label = tk.Label(self.root, text="Velocity Z: ")
        self.velocity_z_label.pack()

        # Labels for additional details
        self.vehicle_mode_label = tk.Label(self.root, text="Vehicle Mode: ")
        self.vehicle_mode_label.pack()
        self.armed_status_label = tk.Label(self.root, text="Armed: ")
        self.armed_status_label.pack()
        self.groundspeed_label = tk.Label(self.root, text="Groundspeed: ")
        self.groundspeed_label.pack()
        self.gps_status_label = tk.Label(self.root, text="GPS Status: ")
        self.gps_status_label.pack()
        self.battery_voltage_label = tk.Label(self.root, text="Battery Voltage: ")
        self.battery_voltage_label.pack()

        # Labels for throttle, yaw, roll, and pitch
        self.throttle_label = tk.Label(self.root, text="Throttle: ")
        self.throttle_label.pack()
        self.yaw_label = tk.Label(self.root, text="Yaw: ")
        self.yaw_label.pack()
        self.roll_label = tk.Label(self.root, text="Roll: ")
        self.roll_label.pack()
        self.pitch_label = tk.Label(self.root, text="Pitch: ")
        self.pitch_label.pack()

        # Labels for Showing the keybindings
        self.show_keybindings_label = tk.Label(self.root, text="Keybindings \n \n")
        self.show_keybindings_label.pack()
        self.show_Control_Guided_label = tk.Label(self.root, text="Control with Guided mode keys \n \n")
        self.show_Control_Guided_label.pack()
        self.show_keygs_label = tk.Label(self.root, text = "U & J for Up & Down \n W & S for Forward and Backward \n A & D for Left and Right \n M for ARM \n Q for Disarm \n L for Land \n N for Takeoff \n P for POSHOLD \n G for GUIDED")
        self.show_keygs_label.pack()

    def update_gui(self):
        try:
            # Access vehicle attributes, and if successful, the vehicle is connected
            altitude = self.vehicle.location.global_relative_frame.alt
            velocity = self.vehicle.velocity
            vehicle_mode = self.vehicle.mode.name
            armed_status = self.vehicle.armed
            groundspeed = self.vehicle.groundspeed
            gps_status = self.vehicle.gps_0.fix_type
            battery_voltage = self.vehicle.battery.voltage
            throttle = self.vehicle.channels['3']  # Assuming throttle is on channel 3
            yaw = self.vehicle.channels['4']  # Assuming yaw is on channel 4
            roll = self.vehicle.channels['1']  # Assuming roll is on channel 1
            pitch = self.vehicle.channels['2']  # Assuming pitch is on channel 2

            # Update GUI labels with vehicle data
            self.connection_label.config(text="Connected")
            self.online_status_label.config(text="Online")
            self.connection_string_label.config(text=f"Connection String: {self.vehicle._master.address}")
            self.altitude_label.config(text=f"Altitude: {altitude:.2f} meters")
            self.velocity_x_label.config(text=f"Velocity X: {velocity[0]:.2f} m/s")
            self.velocity_y_label.config(text=f"Velocity Y: {velocity[1]:.2f} m/s")
            self.velocity_z_label.config(text=f"Velocity Z: {velocity[2]:.2f} m/s")
            self.vehicle_mode_label.config(text=f"Vehicle Mode: {vehicle_mode}")
            self.armed_status_label.config(text=f"Armed: {armed_status}")
            self.groundspeed_label.config(text=f"Groundspeed: {groundspeed:.2f} m/s")
            self.gps_status_label.config(text=f"GPS Status: {gps_status}")
            self.battery_voltage_label.config(text=f"Battery Voltage: {battery_voltage:.2f} V")
            self.throttle_label.config(text=f"Throttle: {throttle}")
            self.yaw_label.config(text=f"Yaw: {yaw}")
            self.roll_label.config(text=f"Roll: {roll}")
            self.pitch_label.config(text=f"Pitch: {pitch}")

        except Exception as e:
            # Handle the exception when the vehicle is disconnected
            self.connection_label.config(text="Disconnected")
            self.online_status_label.config(text="Offline")
            self.connection_string_label.config(text="Connection String: N/A")
            self.altitude_label.config(text="Altitude: N/A")
            self.velocity_x_label.config(text="Velocity X: N/A")
            self.velocity_y_label.config(text="Velocity Y: N/A")
            self.velocity_z_label.config(text="Velocity Z: N/A")
            self.vehicle_mode_label.config(text="Vehicle Mode: N/A")
            self.armed_status_label.config(text="Armed: N/A")
            self.groundspeed_label.config(text="Groundspeed: N/A")
            self.gps_status_label.config(text="GPS Status: N/A")
            self.battery_voltage_label.config(text="Battery Voltage: N/A")
            self.throttle_label.config(text="Throttle: N/A")
            self.yaw_label.config(text="Yaw: N/A")
            self.roll_label.config(text="Roll: N/A")
            self.pitch_label.config(text="Pitch: N/A")

        # Schedule the update every 1000 milliseconds (1 second)
        self.root.after(1000, self.update_gui)

    def start_gui(self):
        # Start the GUI update loop
        self.update_gui()
        self.root.mainloop()
    
    def exit(self):
        self.root.destroy()
        self.vehicle.close()