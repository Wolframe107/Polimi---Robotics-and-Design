//this is the code for the microphone with the running average

#include "RunningAverage.h"
// Define the analog pin connected to the microphone module
const int microphonePin = A0;
RunningAverage myRA(256);

void setup() {
  myRA.clear();
  myRA.fillValue(1024.0f, 256);
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
    float sensorValue = analogRead(microphonePin); // Read the analog value from the microphone
    myRA.addValue(sensorValue);
    Serial.println(myRA.getAverage()); // Print the value to the serial monitor
    //delay(100); // Wait for a short time before reading again
}
