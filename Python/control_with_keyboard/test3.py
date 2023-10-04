from dronekit import connect, VehicleMode
import time
d1 = connect('tcp:127.0.0.1:5762')
while True:
    prev_hearbeat = d1.last_heartbeat
    print('prev',prev_hearbeat)
    time.sleep(5)
    print('last',d1.last_heartbeat)
    if d1.last_heartbeat == prev_hearbeat:
        d1.close()
        print("Reconnecting to drone")
        d1 = connect('tcp:127.0.0.1:5762')
        print("Connected to drone")
    else:
        print("Drone is up to date")
        time.sleep(1)