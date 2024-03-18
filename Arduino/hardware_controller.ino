const int piezo0 = A0; // Analog pin connected to the piezo sensor
const int piezo1 = A1; // Analog pin connected to the piezo sensor
const int piezo2 = A2; // Analog pin connected to the piezo sensor

void setup() {
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "REQUEST") {
      sendDataToPython(); // Send data to Python
    }
  }
}

void sendDataToPython() {
  // Generate some sample data
    int val0 = analogRead(piezo0);
    int val1 = analogRead(piezo1);
    int val2 = analogRead(piezo2);
    Serial.print(val0);
    Serial.print(",");
    Serial.print(val1);
    Serial.print(",");
    Serial.println(val2);
}
