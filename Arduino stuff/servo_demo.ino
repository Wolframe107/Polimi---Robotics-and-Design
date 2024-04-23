#include <Servo.h>


Servo myservo;  // create servo object to control a servo


int potpin = A0;  // analog pin used to connect the potentiometer

int val;    // variable to read the value from the analog pin


void setup() {

  myservo.attach(potpin);  // attaches the servo on pin 9 to the servo object

}


void loop() {
  //myservo.write(0);                  // sets the servo position according to the scaled value

  delay(1000);   
    myservo.write(180);   
                        // waits for the servo to get there
   delay(1000);
     myservo.write(100);   

}