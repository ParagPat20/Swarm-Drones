import keyboard

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
