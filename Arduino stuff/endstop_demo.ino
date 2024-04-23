int pin = 13;  // LED connected to digital pin 13
int val;
void setup() {
  pinMode(pin, INPUT);  // sets the digital pin 13 as output
  Serial.begin(9600);
}

void loop() {
  val = digitalRead(pin);   // read the input pin
  Serial.println(val);
  delay(10);
}