echo "The Server should return: new trip created"
curl -X POST http://localhost:80/trip/start -H "Content-Type: application/json" -d '{"user_id":"1","name":"trip1"}'