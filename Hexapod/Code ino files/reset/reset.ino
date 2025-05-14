#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_MIN 150  // Minimum pulse length
#define SERVO_MAX 600  // Maximum pulse length
#define TOTAL_SERVOS 16

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

void sweepServo(int servoNum, int startAngle, int endAngle) {
  for (int angle = startAngle; angle <= endAngle; angle++) {
    pwm.setPWM(servoNum, 0, map(angle, 0, 180, SERVO_MIN, SERVO_MAX));
    delay(20);
  }
  delay(500);

  for (int angle = endAngle; angle >= startAngle; angle--) {
    pwm.setPWM(servoNum, 0, map(angle, 0, 180, SERVO_MIN, SERVO_MAX));
    delay(20);
  }
  delay(500);
}

void setup() {
  pwm.begin();
  pwm.setPWMFreq(50);  // Analog servos run at 50 Hz
}

void loop() {
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    sweepServo(i, 60, 120);  // Sweep one servo at a time
  }
}
