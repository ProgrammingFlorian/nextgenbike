#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <ESPping.h>

WiFiMulti wifiMulti;

// currently using lab http_request example

const char* ssid = "RK9"; //Your Wifi's SSID
const char* password = "Kaikeong123!"; //Wifi Password
const char* serverAddress = "http://104.248.148.208"; //change to your server's IP


void set_up_server_connection() {

    for(uint8_t t = 4; t > 0; t--) {
        Serial.printf("[SETUP] WAIT %d...\n", t);
        Serial.flush();
        delay(1000);
    }

    wifiMulti.addAP(ssid, password);

    while (wifiMulti.run() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    

    // for testing purposes
    // String start_trip_json_file = create_trip_start_JSON("test_trip", 1);
    // post_request("/trip/start", start_trip_json_file);

    // String end_trip_json_file = create_trip_end_JSON(1);
    // post_request("/trip/end", end_trip_json_file);
}

void put_request(String jsonData) {
  if (WiFi.status() == WL_CONNECTED){
    Serial.println("Sending...");

    HTTPClient http;
    
    String serverURL = serverAddress; //server address
    serverURL += "/sensor"; 
    
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.PUT(jsonData);
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.print("HTTP Request failed: ");
      Serial.println(httpResponseCode);
    }

  } else {
    Serial.println("WiFi disconnected");
  }
  delay(5000);  //Five second delay
}

int post_request(String endpoint, String jsonData) {
  HTTPClient http;
  int trip_id;

  String url = serverAddress + endpoint;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonData);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    String payload = http.getString();
    trip_id = getTripId(payload);
    Serial.println("Response payload: " + payload);
    Serial.println(trip_id);
  } else {
    Serial.print("HTTP Request failed: ");
    Serial.println(httpResponseCode);
  }

  http.end();
  return trip_id;
}