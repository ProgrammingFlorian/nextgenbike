## Server Endpoints

PUT /sensors
{trip_id, acceleration_x, acceleration_y, acceleration_z, gyroscope_x, gyroscope_y, gyroscope_z, vibration, latitude, longitude, crash, user_id}

POST /trip/start
{user_id, name} # TODO: bikeType

POST /trip/end
{trip_id}

IMU: rotation xyz, acceleration xyz
vibration: average, max since last send
location: current location
crash: yes/no
user_id: id
bikeType: {city, trekking, mountain, racing}

the crash is detected on the esp using simple rules:
1. Instantaneous stop
2. falling to the side
3. vibration

What to do with crash data: 
- send GPS position
- phone notification