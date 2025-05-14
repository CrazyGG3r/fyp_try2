#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_MIN 110  // Minimum pulse length count
#define SERVO_MAX 510  // Maximum pulse length count

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Servo channel definitions
#define lcA 0
#define lfA 1
#define ltA 2
#define lcB 3
#define lfB 4
#define ltB 30
#define lcC 5
#define lfC 6
#define ltC 7
#define rcA 8
#define rfA 9
#define rtA 10
#define rcB 11
#define rfB 12
#define rtB 31
#define rcC 13
#define rfC 14
#define rtC 15

void setup() {
  pwm.begin();
  pwm.setPWMFreq(50); // Set frequency to 50 Hz for servos
}

// Move servo to specific angle
void setServoAngle(int channel, int angle) {
  int pulse = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(channel, 0, pulse);
}

// Walking gait function
void walkGait() {
  // Example walking gait sequence
  // Step 1: Lift and move left front leg
  setServoAngle(lfA, 30);
  setServoAngle(lcA, 45);
  delay(200);

  // Step 2: Move right front leg
  setServoAngle(rfA, 30);
  setServoAngle(rcA, 45);
  delay(200);

  // Step 3: Move left middle leg
  setServoAngle(lfB, 30);
  setServoAngle(lcB, 45);
  delay(200);

  // Step 4: Move right middle leg
  setServoAngle(rfB, 30);
  setServoAngle(rcB, 45);
  delay(200);

  // Step 5: Move left rear leg
  setServoAngle(lfC, 30);
  setServoAngle(lcC, 45);
  delay(200);

  // Step 6: Move right rear leg
  setServoAngle(rfC, 30);
  setServoAngle(rcC, 45);
  delay(200);

  // Reset legs to neutral positions
  resetLegs();
}

// Reset all servos to neutral position
void resetLegs() {
  for (int i = 0; i < 16; i++) {
    setServoAngle(i, 90); // Set to neutral position
  }
}

void loop() {
  walkGait();
  delay(1000); // Delay between cycles
}
