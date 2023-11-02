echo "The server should return: New Trip Created with trip_id ..."
echo "currently used: localhost, not used: 146.190.81.3"
curl -X POST http://localhost:80/trip/start -H "Content-Type: application/json" -d '{"name":"test_trip", "user_id":"1"}'