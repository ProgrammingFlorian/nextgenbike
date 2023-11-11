String get_utc_time(unsigned long long &starting_epoch_time) {

  unsigned long long current_epoch_time = starting_epoch_time + millis();

  tmElements_t timeInfo;
  breakTime(current_epoch_time / 1000, timeInfo);
  unsigned long current_millis = current_epoch_time % 1000;

  // Adjust for GMT+8 timezone
  timeInfo.Hour += 8;
  
  // Check if the hour value exceeds 24
  if (timeInfo.Hour >= 24) {
    timeInfo.Hour -= 24;
    timeInfo.Day++;
  }

  // Format the UTC time string
  char utcTime[30];
  snprintf(utcTime, sizeof(utcTime), "%04d-%02d-%02dT%02d:%02d:%02d.%03lu+08:00",
           timeInfo.Year + 1970, timeInfo.Month, timeInfo.Day,
           timeInfo.Hour, timeInfo.Minute, timeInfo.Second, current_millis);
  return utcTime;
}

unsigned long long get_starting_13_digit_epoch(NTPClient &timeClient) {
  timeClient.update();
  unsigned long long actualStartingEpochTime;
  time_t startEpochTime = timeClient.getEpochTime();
  unsigned int startMilliSecs = millis();
  while (true) {
    timeClient.update();
    time_t currentEpochTime = timeClient.getEpochTime();
    if (currentEpochTime - startEpochTime == 1) {
      unsigned int currentMilliSecs = millis();
      unsigned int diffMilliSecs = currentMilliSecs - startMilliSecs;
      actualStartingEpochTime = static_cast<long long>(currentEpochTime) * 1000 - diffMilliSecs;
      break;
    }
  }
  return actualStartingEpochTime;
}
