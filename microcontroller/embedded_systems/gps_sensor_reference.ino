#include <TinyGPSPlus.h>

#define RXD1 16 // Connect NEO-M8 TX to ESP32's RX PIN (16)
#define TXD1 17 // Connect NEO-M8 RX to ESP32'S TX PIN (17)

TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
  delay(3000);
}

void updateSerial(){
  delay(500);
  while (Serial.available())  {
    Serial2.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while (Serial2.available())  {
    Serial.write(Serial2.read());//Forward what Software Serial received to Serial Port
  }
}

void displayInfo()
{
  Serial.print(F("Location: "));
  if (gps.location.isValid()) {
    Serial.print(gps.location.lat(), 10);
    Serial.print(F(","));
    Serial.println(gps.location.lng(), 10);
  }
  else
  {
    Serial.println(F("INVALID"));
  }
  
    delay(500);
}

void loop() {
  //updateSerial();
  while (Serial2.available() > 0)
    if (gps.encode(Serial2.read()))
      displayInfo();
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    delay(2000);
    Serial.println(F("No GPS detected: check wiring."));
  }
}