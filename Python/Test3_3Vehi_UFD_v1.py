from dronekit import connect, VehicleMode, LocationGlobalRelative, Vehicle
from pymavlink import mavutil
import time
import requests
import threading
from flask import Flask, request

app = Flask(__name__)

motor_data = []

@app.route('/motors', methods=['GET', 'POST'])
def motors():
    global motor_data
    if request.method == 'POST':
        motor_data = request.get_json()
        return 'Data received'
    else:
        return {'data': motor_data}

def run_flask_app():
    app.run(host='0.0.0.0')

flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

url = "http://192.168.1.8:5000/motors"

class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)

        self._raw_servo = self.RawSERVO()

        @self.on_message('SERVO_OUTPUT_RAW')
        def listener(self, name, message):
            self._raw_servo.ch1out=message.servo1_raw
            self._raw_servo.ch2out=message.servo2_raw
            self._raw_servo.ch3out=message.servo3_raw
            self._raw_servo.ch4out=message.servo4_raw

            self.notify_attribute_listeners('raw_servo', self._raw_servo) 

    @property
    def raw_servo(self):
        return self._raw_servo
    
    class RawSERVO(object):
        def __init__(self, ch1out=None, ch2out=None, ch3out=None, ch4out=None):
            self.ch1out = ch1out
            self.ch2out = ch2out
            self.ch3out = ch3out
            self.ch4out = ch4out

client = connect('0.0.0.0:14550', wait_ready=True, vehicle_class=MyVehicle)
print("CLIENT connected")

client.mode = VehicleMode("GUIDED_NOGPS")
client.armed = True
while not client.armed:
    time.sleep(1)

def send_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z, duration):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0, 0, 0,
        velocity_x, velocity_y, velocity_z,
        0, 0, 0,
        0, 0)
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def send_data():
    while True:
        try:
            RPM = {
                'ch1out': client.raw_servo.ch1out,
                'ch2out': client.raw_servo.ch2out,
                'ch3out': client.raw_servo.ch3out,
                'ch4out': client.raw_servo.ch4out
            }

            r = requests.post(url, json=RPM)

        except Exception as e:
            print("Error sending data:", str(e))

        time.sleep(0.1)

data_thread = threading.Thread(target=send_data)
data_thread.start()

send_ned_velocity(client, 5, 0, 0, 5)

send_ned_velocity(client,-5 , 0 , 0 ,5)

client.armed = False
while client.armed:
    time.sleep(1)

print("Completed")
client.close()