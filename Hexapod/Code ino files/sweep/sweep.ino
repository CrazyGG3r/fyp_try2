#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define MIN_PULSE_WIDTH 650
#define MAX_PULSE_WIDTH 2350
#define FREQUENCY 50

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int left_coxa[] = {8, 11, 13};
int left_femur[] = {9, 12, 14};
int right_coxa[] = {0, 3, 5};
int right_femur[] = {1, 4, 6};

int f_min_mov = 90;
int f_max_mov = 135;

int c_min_mov = 60;
int c_max_mov = 120;

int min_mov_left = 100;
int min_mov_right = 180 - min_mov_left;

int sweep_delayy = 5;
int delayy = 200;

void moveMotorDegrees(int degree, int motorOut) {
  int pulse_wide = map(degree, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  int pulse_width = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  pwm.setPWM(motorOut, 0, pulse_width);
}
int joint_delay = 5;
void JointSweepTriplet(int start, int endd, int motorA,bool A, int motorB,bool B,int motorC, bool C)
{
  if(start<endd)
  {
   for (int deg = start; deg <= endd; deg++)
   {
    A ? moveMotorDegrees(180-deg,motorA) : moveMotorDegrees(deg,motorA);
    B ? moveMotorDegrees(180-deg,motorB) : moveMotorDegrees(deg,motorB);
    C ? moveMotorDegrees(180-deg,motorC) : moveMotorDegrees(deg,motorC);
    delay(joint_delay);
   }
  }
  else
  {
    for (int deg = start; deg >= endd; deg--)
   {
    A ? moveMotorDegrees(180-deg,motorA) : moveMotorDegrees(deg,motorA);
    B ? moveMotorDegrees(180-deg,motorB) : moveMotorDegrees(deg,motorB);
    C ? moveMotorDegrees(180-deg,motorC) : moveMotorDegrees(deg,motorC);
    delay(joint_delay);
   }
  }
 
}


void tripod_A_up() {
  JointSweepTriplet(f_min_mov, f_max_mov,
                     left_femur[0],false,
                     left_femur[2],false,
                     right_femur[1],true);
}

void tripod_A_backward() {
  JointSweepTriplet(c_min_mov, c_max_mov, 
                    left_coxa[0],false,
                    left_coxa[2],false,
                    right_coxa[1],true);
}
void tripod_A_forward() {
  JointSweepTriplet(c_max_mov, c_min_mov, 
                    left_coxa[0],false,
                    left_coxa[2],false,
                    right_coxa[1],true);
}
void tripod_A_down() {
  JointSweepTriplet(f_max_mov, f_min_mov, 
                    left_femur[0],false,
                    left_femur[2],false,
                    right_femur[1],true);
}

void tripod_B_forward() {
  JointSweepTriplet(c_max_mov, c_min_mov, 
                    left_coxa[1],false,
                    right_coxa[0],true,
                    right_coxa[2],true);
}

void tripod_B_up() {
  JointSweepTriplet(f_min_mov, f_max_mov, 
                    left_femur[1],false,
                    right_femur[0],true,
                    right_femur[2],true);
}

void tripod_B_backward() {
  JointSweepTriplet(c_min_mov, c_max_mov, 
                    left_coxa[1],false,
                    right_coxa[0],true,
                    right_coxa[2],true);
}

void tripod_B_down() {
  JointSweepTriplet(f_max_mov, f_min_mov, 
                    left_femur[1],false,
                    right_femur[0],true,
                    right_femur[2],true);
}



void setup() {
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
  for (int i = 0; i < 3; i++) {
    moveMotorDegrees(c_min_mov, left_coxa[i]);
    moveMotorDegrees(f_min_mov, left_femur[i]);
    moveMotorDegrees(180 - c_min_mov, right_coxa[i]);
    moveMotorDegrees(180 - f_min_mov, right_femur[i]);
  }
}

void loop() {
  tripod_A_up(); delay(delayy);
  tripod_B_backward(); delay(delayy);
  tripod_A_forward(); delay(delayy);
  tripod_A_down(); delay(delayy);
  
  tripod_B_up(); delay(delayy);
  tripod_A_backward(); delay(delayy);
  tripod_B_forward(); delay(delayy);
  tripod_B_down(); delay(delayy);
  
}
