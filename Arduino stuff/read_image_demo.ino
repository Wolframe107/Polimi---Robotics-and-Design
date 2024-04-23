// Example 2 - Receive with an end-marker
#include <Servo.h> 

// Declare the Servo pin 
int servoPin = A1; 
// Create a servo object 
Servo Servo1; 

const byte numChars = 4;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;

void setup() {
    Servo1.attach(servoPin); 
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
}

void loop() {
    recvWithEndMarker();
    moveServo();
    delay(1000);
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

void moveServo() {
    if (newData == true) {
        for(int i = 0; i<numChars; i++){
            if(receivedChars[i] == '0'){
              Serial.print("Zero!");
              Servo1.write(0);
              delay(1000);
            }else{
              Serial.print("One!");
              Servo1.write(180);
              delay(1000);
            }
        }
        newData = false;
    }
}