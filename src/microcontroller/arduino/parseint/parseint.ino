void setup() {
  // initialize serial:
  Serial.begin(9600);
}

void loop() {
  // if there's any serial available, read it:
  while (Serial.available() > 0) {


    int pitch = Serial.parseInt(); 
    int yaw = Serial.parseInt(); 
    int roll = Serial.parseInt(); 
    int z = Serial.parseInt(); 


    if (Serial.read() == '\n') {

      Serial.print(pitch);
      Serial.print (" ");
      Serial.print(yaw);
      Serial.print (" ");
      Serial.print(roll);
      Serial.print (" ");
      Serial.println(z
      );
    }
  }
}

