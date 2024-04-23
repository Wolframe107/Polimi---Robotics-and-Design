#include <Stepper.h>
#include <Servo.h>
#define STEPS 2038
Stepper stepperX(STEPS, 8, 10, 9, 11);
Stepper stepperY(STEPS, 4, 6, 5, 7);
int endstopX = 12;
int endstopY = 13;
int endstopX_val = 1;
int endstopY_val = 1;
int endstopX_val_previous = 1;
int endstopY_val_previous = 1;

int x_dir = -1;
int y_dir = 1;

int x_pos = 0;
int y_pos = 0;
int max_x = 1000;
int max_y = 1000;

int x_test = -100;
int y_test = -100;

int current_dir = 0;

Servo penServo;
int servoPin = A0;

void setup() {
  Serial.begin(9600);
  pinMode(endstopX, INPUT);
  pinMode(endstopY, INPUT);

  stepperX.setSpeed(10);
  stepperY.setSpeed(10);

  penServo.attach(servoPin);
}

void loop() {
  // Read Endstops
  endstopX_val = digitalRead(endstopX);
  endstopY_val = digitalRead(endstopY);
  //Serial.print("Endstop X is: " + String(endstopX_val) + "     ");
  //Serial.println("Endstop Y is: " + String(endstopY_val));

  if(endstopX_val_previous == 1 && endstopX_val == 0 ){
    x_dir *= -1;
    x_test = 0;
    x_pos = 0;
  }

  if(endstopY_val_previous == 1 && endstopY_val == 0){
    y_dir *= -1;
    y_test = 0;
  }

  endstopX_val_previous = endstopX_val;
  endstopY_val_previous = endstopY_val;
  // x plus är 
  penServo.write(180);
  delay(1000);
  stepperX.step(1000 * x_dir);
  delay(1000);
  stepperY.step(500 * y_dir);
  delay(1000);
  stepperX.step(-1000 * x_dir);
  delay(1000);
  stepperY.step(-500 * y_dir);
  delay(1000);
  penServo.write(100);
  delay(1000);
}

void draw_up(int amount){
  if(x_pos > 4000){
    x_dir *= -1;
    x_pos = 0;
  }
  switch (current_dir) {
    case 0:
      draw_up(500);
    case 1:
      draw_left(500);
    case 2:
      draw_down(500);
    case 3:
      draw_right(500);
  }
  stepperY.step(amount * y_dir);
  y_pos += amount;
  current_dir = 1;
}

void draw_left(int amount){
  stepperX.step(amount * x_dir);
  x_pos += amount;
  current_dir = 2;
}

void draw_down(int amount){
  stepperY.step(-amount * y_dir);
  y_pos += amount;
  current_dir = 3;
}

void draw_right(int amount){
  stepperX.step(-amount * x_dir);
  x_pos += amount;
  current_dir = 0;
}
