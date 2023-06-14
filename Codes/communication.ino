#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Servo.h> // Include the Servo library

const char* ssid = "Ardupilot";
const char* password = "ardupilot";
unsigned int localPort = 8888;  // Port to listen on

char packetBuffer[255];  // Buffer to hold incoming packets
WiFiUDP udp;

Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

const int motor1Pin = 2; // GPIO pin for motor 1
const int motor2Pin = 3; // GPIO pin for motor 2
const int motor3Pin = 4; // GPIO pin for motor 3
const int motor4Pin = 5; // GPIO pin for motor 4

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi connected");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(localPort);
  Serial.println("UDP server started");

  motor1.attach(motor1Pin);
  motor2.attach(motor2Pin);
  motor3.attach(motor3Pin);
  motor4.attach(motor4Pin);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.println(packetBuffer);

    // Parse the received packet buffer to get throttle values
    int throttle1, throttle2, throttle3, throttle4;
    sscanf(packetBuffer, "%d,%d,%d,%d", &throttle1, &throttle2, &throttle3, &throttle4);

    // Set the throttle values for each motor
    motor1.writeMicroseconds(throttle1);
    Serial.print("TH1");
    Serial.println(throttle1);
    motor2.writeMicroseconds(throttle2);
    motor3.writeMicroseconds(throttle3);
    motor4.writeMicroseconds(throttle4);
  }
}
