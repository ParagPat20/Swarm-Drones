from dronekit import connect, Vehicle

class RawSERVO(object):
    """
    :param ch1out: servo1
    :param ch2out: servo2
    :param ch3out: servo3
    :param ch4out: servo4
    """
    def __init__(self, ch1out=None, ch2out=None, ch3out=None, ch4out=None):
        """
        RawIMU object constructor.
        """
        self.ch1out = ch1out
        self.ch2out = ch2out
        self.ch3out = ch3out
        self.ch4out = ch4out

    def __str__(self):
        """
        String representation used to print 
        """
        return "{},{},{},{}".format(self.ch1out, self.ch2out, self.ch3out, self.ch4out)


class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)

        # Create an Vehicle.raw_servo object with initial values set to None.
        self._raw_servo = RawSERVO()

        # Create a message listener using the decorator.   
        @self.on_message('SERVO_OUTPUT_RAW')
        def listener(self, name, message):
            """
            The listener is called for messages that contain the string specified in the decorator,
            passing the vehicle, message name, and the message.
            
            The listener writes the message to the (newly attached) ``vehicle.raw_servo`` object 
            and notifies observers.
            """
            self._raw_servo.ch1out=message.servo1_raw
            self._raw_servo.ch2out=message.servo2_raw
            self._raw_servo.ch3out=message.servo3_raw
            self._raw_servo.ch4out=message.servo4_raw

            # Notify all observers of new message (with new value)
            #   Note that argument `cache=False` by default so listeners
            #   are updated with every new message
            self.notify_attribute_listeners('raw_servo', self._raw_servo) 

    @property
    def raw_servo(self):
        return self._raw_servo
    