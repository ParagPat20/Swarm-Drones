#include <Servo.h>

Servo escFrontLeft;   // Create a servo object for the front left ESC
Servo escFrontRight;  // Create a servo object for the front right ESC
Servo escBackLeft;    // Create a servo object for the back left ESC
Servo escBackRight;   // Create a servo object for the back right ESC

const int throttleMin = 1000;   // Minimum pulse width for the RC controller throttle
const int throttleMax = 2000;   // Maximum pulse width for the RC controller throttle
const int escMin = 1000;        // Minimum ESC control signal (adjust if needed)
const int escMax = 2000;        // Maximum ESC control signal (adjust if needed)

const int rollMin = 1000;       // Minimum pulse width for roll control
const int rollMax = 2000;       // Maximum pulse width for roll control
const int pitchMin = 1000;      // Minimum pulse width for pitch control
const int pitchMax = 2000;      // Maximum pulse width for pitch control
const int yawMin = 1000;        // Minimum pulse width for yaw control
const int yawMax = 2000;        // Maximum pulse width for yaw control

int throttle = 1000;            // Initial throttle value
int roll = 1500;                // Initial roll value
int pitch = 1500;               // Initial pitch value
int yaw = 1500;                 // Initial yaw value

void setup() {
  escFrontLeft.attach(9);    // Attach the front left ESC signal wire to digital pin 9
  escFrontRight.attach(10);  // Attach the front right ESC signal wire to digital pin 10
  escBackLeft.attach(11);    // Attach the back left ESC signal wire to digital pin 11
  escBackRight.attach(12);   // Attach the back right ESC signal wire to digital pin 12
  
  escFrontLeft.writeMicroseconds(escMin);    // Send a low signal to start the front left motor off
  escFrontRight.writeMicroseconds(escMin);   // Send a low signal to start the front right motor off
  escBackLeft.writeMicroseconds(escMin);     // Send a low signal to start the back left motor off
  escBackRight.writeMicroseconds(escMin);    // Send a low signal to start the back right motor off
  
  delay(3000);    // Delay for ESC initialization (may vary)
}

void loop() {
  throttle = pulseIn(2, HIGH, 20000);   // Read the pulse width from RC receiver for throttle
  roll = pulseIn(3, HIGH, 20000);       // Read the pulse width from RC receiver for roll
  pitch = pulseIn(4, HIGH, 20000);      // Read the pulse width from RC receiver for pitch
  yaw = pulseIn(5, HIGH, 20000);        // Read the pulse width from RC receiver for yaw

  // Map the pulse width range from RC receiver to respective control signals
  int escFrontLeftSignal = throttle;
  int escFrontRightSignal = throttle;
  int escBackLeftSignal = throttle;
  int escBackRightSignal = throttle;

  // Adjust the front and back motor speeds based on roll, pitch, and yaw inputs
  escFrontLeftSignal += map(roll, rollMin, rollMax, -200, 200);        // Adjust roll control signal for front left motor
  escFrontRightSignal -= map(roll, rollMin, rollMax, -200, 200);       // Adjust roll control signal for front right motor
  escFrontLeftSignal += map(pitch, pitchMin, pitchMax, -200, 200);     // Adjust pitch control signal for front left motor
  escFrontRightSignal += map(pitch, pitchMin, pitchMax, -200, 200);    // Adjust pitch control signal for front right motor
  escBackLeftSignal -= map(yaw, yawMin, yawMax, -200, 200);            // Adjust yaw control signal for back left motor
  escBackRightSignal += map(yaw, yawMin, yawMax, -200, 200);           // Adjust yaw control signal for back right motor

  // Limit the ESC signals within the specified range
  escFrontLeftSignal = constrain(escFrontLeftSignal, escMin, escMax);
  escFrontRightSignal = constrain(escFrontRightSignal, escMin, escMax);
  escBackLeftSignal = constrain(escBackLeftSignal, escMin, escMax);
  escBackRightSignal = constrain(escBackRightSignal, escMin, escMax);

  // Send the control signals to the respective ESCs
  escFrontLeft.writeMicroseconds(escFrontLeftSignal);    // Control the front left motor
  escFrontRight.writeMicroseconds(escFrontRightSignal);  // Control the front right motor
  escBackLeft.writeMicroseconds(escBackLeftSignal);      // Control the back left motor
  escBackRight.writeMicroseconds(escBackRightSignal);    // Control the back right motor
}
