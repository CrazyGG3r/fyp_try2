#include <WiFi.h>
//connection stuff
const char* ssid = "DEEZ_NUTSS";
const char* password = "12345678";
const uint16_t serverPort = 1234;
WiFiClient client;
//0---=-=-=-=-

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

void step_fd()
{
   tripod_A_up(); delay(delayy);
  tripod_B_backward(); delay(delayy);
  tripod_A_forward(); delay(delayy);
  tripod_A_down(); delay(delayy);
  
  tripod_B_up(); delay(delayy);
  tripod_A_backward(); delay(delayy);
  tripod_B_forward(); delay(delayy);
  tripod_B_down(); delay(delayy);
  
}
void step_bk()
{
  tripod_A_up(); delay(delayy);
  tripod_B_forward(); delay(delayy);
  tripod_A_backward(); delay(delayy);
  tripod_A_down(); delay(delayy);
  
  tripod_B_up(); delay(delayy);
  tripod_A_forward(); delay(delayy);
  tripod_B_backward(); delay(delayy);
  tripod_B_down(); delay(delayy);
}
// Move a single coxa joint
void moveCoxaJoint(int motor, bool isRight, int startDeg, int endDeg) {
  if(startDeg < endDeg) {
    for (int deg = startDeg; deg <= endDeg; deg++) {
      isRight ? moveMotorDegrees(180-deg, motor) : moveMotorDegrees(deg, motor);
      delay(joint_delay);
    }
  } else {
    for (int deg = startDeg; deg >= endDeg; deg--) {
      isRight ? moveMotorDegrees(180-deg, motor) : moveMotorDegrees(deg, motor);
      delay(joint_delay);
    }
  }
}

void step_right()
{
  // Rotate right (clockwise)
  // First tripod (legs 1, 3, 5)
  tripod_A_up(); delay(delayy);
  
  // Move right leg of tripod A backward
  moveCoxaJoint(right_coxa[1], true, c_min_mov, c_max_mov);
  
  // Move left legs of tripod A forward
  moveCoxaJoint(left_coxa[0], false, c_max_mov, c_min_mov);
  moveCoxaJoint(left_coxa[2], false, c_max_mov, c_min_mov);
  
  tripod_A_down(); delay(delayy);
  
  // Second tripod (legs 2, 4, 6)
  tripod_B_up(); delay(delayy);
  
  // Move right legs of tripod B backward
  moveCoxaJoint(right_coxa[0], true, c_min_mov, c_max_mov);
  moveCoxaJoint(right_coxa[2], true, c_min_mov, c_max_mov);
  
  // Move left leg of tripod B forward
  moveCoxaJoint(left_coxa[1], false, c_max_mov, c_min_mov);
  
  tripod_B_down(); delay(delayy);
}

void step_left()
{
  // Rotate left (counter-clockwise)
  // First tripod (legs 1, 3, 5)
  tripod_A_up(); delay(delayy);
  
  // Move right leg of tripod A forward
  moveCoxaJoint(right_coxa[1], true, c_max_mov, c_min_mov);
  
  // Move left legs of tripod A backward
  moveCoxaJoint(left_coxa[0], false, c_min_mov, c_max_mov);
  moveCoxaJoint(left_coxa[2], false, c_min_mov, c_max_mov);
  
  tripod_A_down(); delay(delayy);
  
  // Second tripod (legs 2, 4, 6)
  tripod_B_up(); delay(delayy);
  
  // Move right legs of tripod B forward
  moveCoxaJoint(right_coxa[0], true, c_max_mov, c_min_mov);
  moveCoxaJoint(right_coxa[2], true, c_max_mov, c_min_mov);
  
  // Move left leg of tripod B backward
  moveCoxaJoint(left_coxa[1], false, c_min_mov, c_max_mov);
  
  tripod_B_down(); delay(delayy);
}
void stand()
{
   for (int i = 0; i < 3; i++) {
    moveMotorDegrees(c_min_mov, left_coxa[i]);
    moveMotorDegrees(f_min_mov, left_femur[i]);
    moveMotorDegrees(180 - c_min_mov, right_coxa[i]);
    moveMotorDegrees(180 - f_min_mov, right_femur[i]);
  }
}
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  while (!client.connect("192.168.137.1", serverPort)) {
    Serial.println("Trying to connect to server...");
    delay(1000);
  }
  Serial.println("Connected to server, now standing up");
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
  stand(); 
}

  void loop() {
    if (client.connected() && client.available()) {
      String msg = client.readStringUntil('\n');
      msg = msg.substring(1);
       msg.trim();
      Serial.print("Received: ");
      Serial.println(msg);
  
      if (msg == "FD") {
        step_fd();
        stand();
        Serial.println("FORWARD");
        client.println("DONE _ FORWARD");
      }
  
      if (msg == "BK") {
         step_bk();
         stand();
        Serial.println("BACKWARD");
        client.println("DONE _ BACKWARD");
      }
      if (msg == "RT") {
         step_right();
         stand();
        Serial.println("RIGHT");
        client.println("DONE _ RIGHT");
      }
      if (msg == "LT") {
         step_left();
         stand();
        Serial.println("LEFT");
        client.println("DONE _ LEFT");

      }
    }
  }
