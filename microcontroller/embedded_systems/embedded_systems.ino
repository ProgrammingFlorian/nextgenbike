#define SWITCH 4
#define vibrationPin 15 
#define RXD1 16 // Connect NEO-M8 TX to ESP32's RX PIN (16)
#define TXD1 17 // Connect NEO-M8 RX to ESP32'S TX PIN (17)

#include <vector>
#include "Wire.h"
#include "I2Cdev.h"
#include "ADXL345.h"
#include "ITG3200.h"
#include "TimeLib.h"
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>


std::vector<float> latitudeData;
std::vector<float> longitudeData;
std::vector<float> vibrationData;
std::vector<float> accelerationXData;
std::vector<float> accelerationYData;
std::vector<float> accelerationZData;
std::vector<float> gyroscopeXData;
std::vector<float> gyroscopeYData;
std::vector<float> gyroscopeZData;
std::vector<String> dateTimeData;

ADXL345 accel;
ITG3200 gyro;
TinyGPSPlus gps;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");
SoftwareSerial ss(RXD1, TXD1);

volatile bool switch_state = LOW;
bool is_data_generated = false;
int trip_count = 0;
int16_t ax, ay, az;
int16_t gx, gy, gz;
double latitude, longitude;
int loop_count = 0;
unsigned long long starting_epoch_time;
int trip_id;
unsigned long lastDebounceTime = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ss.begin(9600);
  pinMode(SWITCH, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(SWITCH), switchInterrupt, CHANGE);
  set_up_server_connection();
  Wire.begin();
  accel.initialize();
  gyro.initialize();
  timeClient.begin();

  // Wait for the time to be synchronized
  while (!timeClient.update()) {
    Serial.println("Updating time...");
    timeClient.forceUpdate();
    delay(100);
  }
  Serial.println("Time updated");

  starting_epoch_time = get_starting_13_digit_epoch(timeClient);

  Serial.println("Testing device connections...");
  Serial.println(accel.testConnection() ? "ADXL345 connection successful" : "ADXL345 connection failed");
  Serial.println(gyro.testConnection() ? "ITG3200 connection successful" : "ITG3200 connection failed");


}

void loop() {
    // Fetch data from GPS sensor
  while (ss.available() > 0) {
    if (gps.encode(ss.read())) {
      if (gps.location.isValid()) {
        latitude = gps.location.lat();
        longitude = gps.location.lng();
        Serial.println("Latitude");
        Serial.println(latitude, 10);
      }
    }
  }


  // // // record data when switch is on
  if (switch_state) {
    // wakeup

    if (!is_data_generated) {
      String start_trip_json_file = create_trip_start_JSON("data_collection", 1);
      trip_id = post_request("/trip/start", start_trip_json_file);
    }
    is_data_generated = true;

    // get output from sensors
    double vibration_output = digitalRead(vibrationPin);
    accel.getAcceleration(&ax, &ay, &az);
    gyro.getRotation(&gx, &gy, &gz);    
    String utc_time = get_utc_time(starting_epoch_time);

    // store output into an array
    vibrationData.push_back(vibration_output);
    accelerationXData.push_back(ax);
    accelerationYData.push_back(ay);
    accelerationZData.push_back(az);
    gyroscopeXData.push_back(gx);
    gyroscopeYData.push_back(gy);
    gyroscopeZData.push_back(gz);
    latitudeData.push_back(latitude);
    longitudeData.push_back(longitude);
    dateTimeData.push_back(utc_time); 

    if (loop_count % 10 == 0) {
      String datajsonFile = create_sensor_JSON_data(trip_id, latitudeData, longitudeData, vibrationData,
                                              accelerationXData, accelerationYData, accelerationZData,
                                              gyroscopeXData, gyroscopeYData, gyroscopeZData, dateTimeData);
      put_request(datajsonFile);
      vibrationData.clear();
      accelerationXData.clear();
      accelerationYData.clear();
      accelerationZData.clear();
      gyroscopeXData.clear();
      gyroscopeYData.clear();
      gyroscopeZData.clear();
      latitudeData.clear();
      longitudeData.clear();
      dateTimeData.clear();
      // put to sleep
      // Serial.println(loop_count);
    }

    loop_count++;
  }

  // // Off switch indicates end of trip and do post request to trip/end using trip_id received
  if (!switch_state && is_data_generated) {
      String end_trip_json_file = create_trip_end_JSON(trip_id);
      // String end_trip_json_file = create_trip_end_JSON(trip_id);
      post_request("/trip/end", end_trip_json_file);
      is_data_generated = false;
      // go to sleep
  }

  //delay for 0.05s so that it samples at a 20hz rate
  delay(50); 
}

void switchInterrupt() {
  // Check if enough time has passed since the last state change
  if ((millis() - lastDebounceTime) >= 200) {
    lastDebounceTime = millis();
    // Update the switch state
    switch_state = !switch_state;

  }
}