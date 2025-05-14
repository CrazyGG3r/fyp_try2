#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 150   // Adjust for full 0-degree position
#define SERVOMAX 650   // Adjust for full 180-degree position
#define NUM_LEGS 6     // Hexapod has 6 legs (but missing right_tibia_B & left_tibia_B)
#define STEP_DELAY 200 // Delay between movements

// Leg groupings for the tripod gait (excluding right_tibia_B and left_tibia_B)

int base_Set_1_coxa[] = {0, 11, 5};
int base_Set_1_femur[] = {1, 12, 6};
int base_Set_2_coxa[] = {8, 3, 13};
int base_Set_2_femur[] = {9, 4, 14};
int tibias[] = {2, 7, 10, 15};

int delaay = 1000;

uint16_t angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
  
}

void setup() {
  Serial.begin(9600);
  Wire.begin(21, 22);  // ESP32 I2C: SDA=21, SCL=22
  pwm.begin();
  pwm.setPWMFreq(50);  // 50Hz for servos
  Serial.println("Starting tripod gait (adjusted)...");
  delay(500);
  moveSet(base_Set_1_coxa, 90);
  delay(300);
  moveSet(base_Set_1_femur, 0);
  delay(300);
  moveSet(base_Set_2_coxa, 90);
  delay(300);
  moveSet(base_Set_2_femur, 0);
  delay(300);
  moveSet(tibias, 0);
}

void moveSet(int set[], int angle) {
  for (int i = 0; i < 3; i++) {
    pwm.setPWM(set[i], 0, angleToPulse(angle));
  }
}

void tri_walk()
{
  moveSet(base_Set_1_femur, 45);
  delay(delaay);
  moveSet(base_Set_1_coxa, 45);
  delay(delaay);
  moveSet(base_Set_2_coxa, 135);
  delay(delaay);
  moveSet(base_Set_1_femur, 0);
  delay(delaay);
  moveSet(base_Set_2_femur, 45);
  delay(delaay);
  moveSet(base_Set_1_femur, 135);
  delay(delaay);
  moveSet(base_Set_2_coxa, 45);
  delay(delaay);
  moveSet(base_Set_2_femur, 0);
  delay(delaay);
}

void loop() {
  // Step 1: Lift & Move group A forward


  tri_walk();
}
