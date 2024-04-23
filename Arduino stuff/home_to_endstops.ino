#include <Stepper.h>
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

void setup() {
  Serial.begin(9600);
  pinMode(endstopX, INPUT);
  pinMode(endstopY, INPUT);

  stepperX.setSpeed(15);
  stepperY.setSpeed(15);
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
  }

  if(endstopY_val_previous == 1 && endstopY_val == 0){
    y_dir *= -1;
    y_test = 0;
  }

  endstopX_val_previous = endstopX_val;
  endstopY_val_previous = endstopY_val;

  // Move X axis to 0 and stop
  if(x_test != 0){
    stepperX.step(-50 * x_dir);
  }

  if(y_test != 0){
    stepperY.step(-50 * y_dir);
  }
  
  // Move Y axis to 0 and stop

}
