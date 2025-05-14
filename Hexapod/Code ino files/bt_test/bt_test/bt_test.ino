#include <WiFi.h>
#include <Adafruit_PWMServoDriver.h>

const char* ssid = "DEEZ_NUTSS";
const char* password = "12345678";

const char* serverIP = "192.168.137.1";  // Change to your laptop's local IP
const int serverPort = 9999;

WiFiClient client;
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define SERVO_MIN 120  // Min pulse length
#define SERVO_MAX 650  // Max pulse length

// Define servo channels (0-15 for PCA9685, total 15 channels used)
const int servo_channels[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
const int num_servos = sizeof(servo_channels) / sizeof(servo_channels[0]);

void setup() {
    Serial.begin(115200);
    pwm.begin();
    pwm.setPWMFreq(50); // Set frequency for servos
    
    WiFi.begin(ssid, password);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to Wi-Fi");
    Serial.print("ESP32 IP: ");
    Serial.println(WiFi.localIP());

    Serial.print("Connecting to server...");
    while (!client.connect(serverIP, serverPort)) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("\nConnected to Python Server!");
}


uint16_t angleToPulse(int angle) {
  return map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
}

void resetPosition(int angle) {
    for (int i = 0; i < num_servos; i++) {
        pwm.setPWM(set[i], 0, angleToPulse(angle));
  }
    }
    Serial.println("Reset to base position");
}

void sweepMotion() {
    for (int i = 0; i < num_servos; i++) {
        pwm.setPWM(servo_channels[i], 0, SERVO_MIN);
    }
    delay(500);
    for (int i = 0; i < num_servos; i++) {
        pwm.setPWM(servo_channels[i], 0, SERVO_MAX);
    }
    delay(500);
    Serial.println("Sweep motion completed");
}

void forwardMotion() {
    // Placeholder for tripod gait movement
    Serial.println("Walking forward...");
}

void loop() {
    if (client.connected()) {
        if (client.available()) {
            String command = client.readStringUntil('\n');
            command.trim();
            Serial.print("Received: ");
            Serial.println(command);
            
            if (command == "reset") {
                resetPosition(60);
            } else if (command == "sweep") {
                sweepMotion();
            } else if (command == "forward") {
                forwardMotion();
            }
        }
    } else {
        Serial.println("Disconnected! Reconnecting...");
        while (!client.connect(serverIP, serverPort)) {
            delay(1000);
        }
        Serial.println("Reconnected!");
    }
}
