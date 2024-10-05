// Example for a receiving script

void setup() {
  // initialize serial:
  Serial.begin(9600);
  // make the pins outputs:
  pinMode(13, OUTPUT); // Pin 13 wird als Ausgang definiert

}

void loop() {
  // if there's any serial available, read it:
  while (Serial.available() > 0) {

    String request = Serial.readStringUntil('\r');
    request.trim();

    if (request == "Test") {

      digitalWrite(13, HIGH); // make the led blink
      delay(1000);
      digitalWrite(13, LOW);   
  
    }
  }
}
