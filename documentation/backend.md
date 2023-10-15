## Server Endpoints

PUT /sensors
{imu, vibration, location, crash, userID}

POST /trip/start
{userID, bikeType}

POST /trip/end
{userID}

IMU: rotation xyz, acceleration xyz
vibration: average, max since last send
location: current location
crash: yes/no
userID: id
bikeType: {city, trekking, mountain, racing}

the crash is detected on the esp using simple rules:
1. Instantaneous stop
2. falling to the side
3. vibration