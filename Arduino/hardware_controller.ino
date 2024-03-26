#include <Adafruit_NeoPixel.h>

#define LED_PIN_0 6   // Pin connected to the first NeoPixel strip
#define LED_PIN_1 7   // Pin connected to the second NeoPixel strip
#define LED_PIN_2 8  // Pin connected to the third NeoPixel strip
#define NUM_PIXELS 4  // Number of NeoPixels in each strip

// Initialize NeoPixel strips
Adafruit_NeoPixel panel_0(NUM_PIXELS, LED_PIN_0, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel panel_1(NUM_PIXELS, LED_PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel panel_2(NUM_PIXELS, LED_PIN_2, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600); // Initialize serial communication
  panel_0.begin();     // Initialize panel_0
  panel_1.begin();     // Initialize panel_1
  panel_2.begin();     // Initialize panel_2
  panel_0.show();      // Initialize all strips to off
  panel_1.show();
  panel_2.show();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("on")) {
      int panelNumber = command.substring(3).toInt(); // Extract panel number from command
      illuminatePanel(panelNumber); // Illuminate the selected panel
    } else if (command.startsWith("off")) {
      turnOffAllStrips(); // Turn off all NeoPixel strips
    }
  }
}

void illuminatePanel(int panelNumber) {
  switch (panelNumber) {
    case 0:
      illuminate(panel_0);
      break;
    case 1:
      illuminate(panel_1);
      break;
    case 2:
      illuminate(panel_2);
      break;
    default:
      // Invalid panel number, do nothing
      break;
  }
}

void illuminate(Adafruit_NeoPixel& panel) {
  for (int i = 0; i < panel.numPixels(); i++) {
    panel.setPixelColor(i, panel.Color(255, 255, 255)); // Set color to white
  }
  panel.show();
}

void turnOffAllStrips() {
  panel_0.clear(); // Clear all pixels in panel_0
  panel_1.clear(); // Clear all pixels in panel_1
  panel_2.clear(); // Clear all pixels in panel_2
  panel_0.show();  // Update panel_0
  panel_1.show();  // Update panel_1
  panel_2.show();  // Update panel_2
}