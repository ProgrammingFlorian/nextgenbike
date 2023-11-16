#include <ArduinoJson.h>

String create_sensor_JSON_data(int tripId, std::vector<float> latitude, std::vector<float> longitude, std::vector<float> vibration,
                          std::vector<float> accelerationX, std::vector<float> accelerationY, std::vector<float> accelerationZ,
                          std::vector<float> gyroscopeX, std::vector<float> gyroscopeY, std::vector<float> gyroscopeZ, std::vector<String> dateTimeData) {
  DynamicJsonDocument jsonDoc(1024);
  jsonDoc["trip_id"] = tripId;

  JsonArray latitudejsonArray = jsonDoc.createNestedArray("latitude");
  JsonArray longitudejsonArray = jsonDoc.createNestedArray("longitude");
  JsonArray vibrationjsonArray = jsonDoc.createNestedArray("vibration");
  JsonArray accelerationXjsonArray = jsonDoc.createNestedArray("acceleration_x");
  JsonArray accelerationYjsonArray = jsonDoc.createNestedArray("acceleration_y");
  JsonArray accelerationZjsonArray = jsonDoc.createNestedArray("acceleration_z");
  JsonArray gyroscopeXjsonArray = jsonDoc.createNestedArray("gyroscope_x");
  JsonArray gyroscopeYjsonArray = jsonDoc.createNestedArray("gyroscope_y");
  JsonArray gyroscopeZjsonArray = jsonDoc.createNestedArray("gyroscope_z");
  JsonArray dateTimejsonArray = jsonDoc.createNestedArray("time");
  
  size_t size = vibration.size();
  for(size_t i = 0; i < size; i++) {
    latitudejsonArray.add(latitude[i]);
    longitudejsonArray.add(longitude[i]);
    vibrationjsonArray.add(vibration[i]);
    accelerationXjsonArray.add(accelerationX[i]);
    accelerationYjsonArray.add(accelerationY[i]);
    accelerationZjsonArray.add(accelerationZ[i]);
    gyroscopeXjsonArray.add(gyroscopeX[i]);
    gyroscopeYjsonArray.add(gyroscopeY[i]);
    gyroscopeZjsonArray.add(gyroscopeZ[i]);
    dateTimejsonArray.add(dateTimeData[i]);  }

  String jsonString;
  serializeJson(jsonDoc, jsonString);

  return jsonString;
}

String create_trip_end_JSON(int trip_id) {
  DynamicJsonDocument jsonDoc(512);
  jsonDoc["trip_id"] = trip_id;
  String jsonString;
  serializeJson(jsonDoc, jsonString);

  return jsonString;
}

String create_trip_start_JSON(String trip_name, int user_id) {
  DynamicJsonDocument jsonDoc(512);
  jsonDoc["name"] = trip_name;
  jsonDoc["user_id"] = user_id;
  String jsonString;
  serializeJson(jsonDoc, jsonString);

  return jsonString;
}

int getTripId(String payload) {
  DynamicJsonDocument doc(256);

  // Parse the JSON payload
  DeserializationError error = deserializeJson(doc, payload);

  // Check for parsing errors
  if (error) {
    Serial.print("JSON parsing failed: ");
    Serial.println(error.c_str());
    return -1;  // Or some error value
  }

  // Extract the trip_id
  int tripId = doc["trip_id"];

  return tripId;
}