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

    def takeoff(self, aTargetAltitude):
        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude)
        while True:
            current_altitude = self.vehicle.location.global_relative_frame.alt
            if current_altitude is not None:
                print(" Altitude: ", current_altitude)
                if current_altitude >= aTargetAltitude * 0.8:
                    print("Reached target altitude")
                    break
                if keyboard.is_pressed('b'):
                    self.vehicle.mode = VehicleMode('LAND')
                    break
            else:
                print("Waiting for altitude information...")
            time.sleep(1)
    
    def takeoff_channel(self, aTargetAltitude):
        print("Taking off!")
        throttle_channel = 3  # Throttle channel
        throttle_increment = 30  # Increment in throttle value]
        throttle = 1000
        self.arm(mode='STABILIZE')
        current_throttle = throttle
        self.vehicle.channels.overrides[throttle_channel] = current_throttle
        while self.vehicle.location.global_relative_frame.alt < aTargetAltitude:
            current_altitude = self.vehicle.location.global_relative_frame.alt
            print(f"Current Altitude: {current_altitude} meters")

        # Incrementally increase throttle
            new_throttle = min(current_throttle + throttle_increment, 2000)
            current_throttle = new_throttle
        # Set channel override for throttle
            self.vehicle.channels.overrides[throttle_channel] = new_throttle
            time.sleep(1)

            if current_altitude >= aTargetAltitude * 0.8:
                    print("Reached target altitude")
                    break

            if keyboard.is_pressed('b'):
                    self.vehicle.mode = VehicleMode('LAND')
                    break
        self.vehicle.mode = VehicleMode('GUIDED')
        print("Reached target altitude. Hovering...")
        self.vehicle.channels.overrides[throttle_channel] = 1500
        self.control_with_keyboard()

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
        MAX_VELOCITY = 0.5

        print("Use arrow keys to control the drone. Press 'Esc' to exit.")

        while True:
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
            if keyboard.is_pressed('m'):
                self.arm()
            if keyboard.is_pressed('n'):
                self.takeoff_channel(1)
            if keyboard.is_pressed('l'):
                self.land()
            if keyboard.is_pressed('q'):
                self.disarm()
            
            if keyboard.is_pressed('p'):
                self.control_stabilized()

            # Exit the loop if the 'Esc' key is pressed
            if keyboard.is_pressed('esc'):
                self.send_ned_velocity(0, 0, 0, 1)  # Stop the drone before exiting
                print("Can not control the drone anymore")
                break
    def control_stabilized(self):
        ROLL = 1500
        PITCH = 1500
        YAW = 1500
        THROTTLE = 1000
        last_w_press_time = 0
        last_s_press_time = 0
        last_a_press_time = 0
        last_d_press_time = 0
        last_q_press_time = 0
        last_e_press_time = 0
        last_u_press_time = 0
        last_j_press_time = 0
        delay = 0.2  # Adjust the delay time as needed (in seconds)
        self.vehicle.channels.overrides[1,2,3,4] = [1500,1500,1000,1500]
        while True:
            # Initialize Channels
            if keyboard.is_pressed('u'):
                current_time = time.time()
                if current_time - last_u_press_time >= delay:
                    THROTTLE +=20
                    self.vehicle.channels.overrides[3] = min(THROTTLE,1000,max(THROTTLE,2000))
                    last_u_press_time = current_time
            
            if keyboard.is_pressed('j'):
                current_time = time.time()
                if current_time - last_j_press_time >= delay:
                    THROTTLE -=20
                    self.vehicle.channels.overrides[3] = min(THROTTLE,1000,max(THROTTLE,2000))
                    last_j_press_time = current_time

            if keyboard.is_pressed('w'):
                current_time = time.time()
                if current_time - last_w_press_time >= delay:
                    PITCH -=20
                    self.vehicle.channels.overrides[2] = min(PITCH,1000,max(PITCH,2000))
                    last_w_press_time = current_time
                else:
                    self.vehicle.channels.overrides[2] = 1500
            
            if keyboard.is_pressed('s'):
                current_time = time.time()
                if current_time - last_s_press_time >= delay:
                    PITCH +=20
                    self.vehicle.channels.overrides[2] = min(PITCH,1000,max(PITCH,2000))
                    last_s_press_time = current_time
                else:
                    self.vehicle.channels.overrides[2] = 1500

            if keyboard.is_pressed('a'):
                current_time = time.time()
                if current_time - last_a_press_time >= delay:
                    ROLL -=20
                    self.vehicle.channels.overrides[1] = min(ROLL,1000,max(ROLL,2000))
                    last_a_press_time = current_time
                else:
                    self.vehicle.channels.overrides[1] = 1500
                
            if keyboard.is_pressed('d'):
                current_time = time.time()
                if current_time - last_d_press_time >= delay:
                    ROLL +=20
                    self.vehicle.channels.overrides[1] = min(ROLL,1000,max(ROLL,2000))
                    last_d_press_time = current_time
                else:
                    self.vehicle.channels.overrides[1] = 1500

            if keyboard.is_pressed('q'):
                current_time = time.time()
                if current_time - last_q_press_time >= delay:
                    YAW -=20
                    self.vehicle.channels.overrides[4] = min(YAW,1000,max(YAW,2000))
                    last_q_press_time = current_time
                else:
                    self.vehicle.channels.overrides[4] = 1500

            if keyboard.is_pressed('e'):
                current_time = time.time()
                if current_time - last_e_press_time >= delay:
                    YAW +=20
                    self.vehicle.channels.overrides[4] = min(YAW,1000,max(YAW,2000))
                    last_e_press_time = current_time
                else:
                    self.vehicle.channels.overrides[4] = 1500

            if keyboard.is_pressed('x'):
                self.arm(mode='STABILIZE')
            
            if keyboard.is_pressed('z'):
                self.disarm()

            if keyboard.is_pressed('l'):
                self.land()

            # write an autotune code for the vehicle
            if keyboard.is_pressed('m'):
                self.vehicle.mode = VehicleMode('POSHOLD')
                time.sleep(5)
                self.vehicle.mode = VehicleMode('AUTOTUNE')
                time.sleep(5)
                self.vehicle.channels.overrides[2] = 1300
                time.sleep(1)
                self.vehicle.channels.overrides[2] = 1700
                time.sleep(1)
                self.vehicle.channels.overrides[2] = 1500
                time.sleep(2)
                self.vehicle.mode = VehicleMode('POSHOLD')
                time.sleep(5)
                self.vehicle.mode = VehicleMode('AUTOTUNE')
                time.sleep(5)
                self.vehicle.channels.overrides[1] = 1300
                time.sleep(1)
                self.vehicle.channels.overrides[1] = 1700
                time.sleep(1)
                self.vehicle.channels.overrides[1] = 1500
                time.sleep(2)
                self.vehicle.mode = VehicleMode('POSHOLD')
                time.sleep(5)
                self.vehicle.mode = VehicleMode('AUTOTUNE')
                time.sleep(5)
                self.vehicle.channels.overrides[4] = 1300
                time.sleep(1)
                self.vehicle.channels.overrides[4] = 1700
                time.sleep(1)
                self.vehicle.channels.overrides[4] = 1500
                time.sleep(2)
                self.vehicle.mode = VehicleMode('POSHOLD')
                time.sleep(5)


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

        # Schedule the update every 1000 milliseconds (1 second)
        self.root.after(1000, self.update_gui)

    def start_gui(self):
        # Start the GUI update loop
        self.update_gui()
        self.root.mainloop()
    
    def exit(self):
        self.root.destroy()
        self.vehicle.close()
