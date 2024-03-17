const int piezo0 = A0; // Analog pin connected to the piezo sensor
const int piezo1 = A1; // Analog pin connected to the piezo sensor
const int piezo2 = A2; // Analog pin connected to the piezo sensor

int val0 = 0;
int val1 = 0;
int val2 = 0;

void setup() {
  Serial.begin(9600);
}
void loop() {
    val0 = analogRead(piezo0);
    val1 = analogRead(piezo1);
    val2 = analogRead(piezo2);
    Serial.print("[");
    Serial.print(val0);
    Serial.print(",");
    Serial.print(val1);
    Serial.print(",");
    Serial.println(val2);
}
