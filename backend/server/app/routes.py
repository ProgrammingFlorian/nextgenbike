import json
from datetime import datetime

from app.extensions import db
from app.models import User, Trip, Sensors
from flask import request, Blueprint
from marshmallow import Schema, ValidationError, fields

url = Blueprint('urls', __name__)


class CreateUserSchema(Schema):
    username = fields.String(required=True)


class TripStartSchema(Schema):
    name = fields.String(required=True)
    user_id = fields.Integer(required=True)


class TripEndSchema(Schema):
    trip_id = fields.Integer(required=True)


class SensorSchema(Schema):
    trip_id = fields.Integer(required=True)
    time = fields.List(fields.DateTime, required=True)

    vibration = fields.List(fields.Float, required=True)

    latitude = fields.List(fields.Float, required=True)
    longitude = fields.List(fields.Float, required=True)

    acceleration_x = fields.List(fields.Float, required=True)
    acceleration_y = fields.List(fields.Float, required=True)
    acceleration_z = fields.List(fields.Float, required=True)
    gyroscope_x = fields.List(fields.Float, required=True)
    gyroscope_y = fields.List(fields.Float, required=True)
    gyroscope_z = fields.List(fields.Float, required=True)

    crash = fields.Integer(required=False)
    terrain = fields.Integer(required=False)


@url.route('/')
@url.route('/index')
def index():
    return 'Hello, World!'


@url.route('/users', methods=['POST'])
def users():
    schema = CreateUserSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        print(f"ValidationError {err}")
        return json.dumps(err.messages), 400
    print(f"Received request with payload {data}")

    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()

    response = json.dumps({"user_id": user.id})

    return response, 200


@url.route('/trip/start', methods=['POST'])
def trip_start():
    schema = TripStartSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {data}")

    trip = Trip(name=data['name'], user_id=data['user_id'])
    db.session.add(trip)
    db.session.commit()

    response = json.dumps({"trip_id": trip.id})

    return response, 200


@url.route('/trip/end', methods=['POST'])
def trip_end():
    schema = TripEndSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {data}")

    trip = db.session.execute(db.select(Trip).filter_by(id=data['trip_id'])).scalar_one()
    trip.end = datetime.utcnow()

    db.session.commit()

    response = f"Finished trip {trip.id} at {trip.end}"

    return response, 200


@url.route('/sensor', methods=['PUT'])
def sensor():
    schema = SensorSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {data}")

    for i in range(len(data['time'])):
        sensor_row = Sensors(time=data['time'][i], trip_id=data['trip_id'], vibration=data['vibration'][i],
                             latitude=data['latitude'][i], longitude=data['longitude'][i],
                             acceleration_x=data['acceleration_x'][i], acceleration_y=data['acceleration_y'][i],
                             acceleration_z=data['acceleration_z'][i], gyroscope_x=data['gyroscope_x'][i],
                             gyroscope_y=data['gyroscope_y'][i], gyroscope_z=data['gyroscope_z'][i])
        db.session.add(sensor_row)

    db.session.commit()

    return 'Submitted sensor data', 200


@url.route('/sensor', methods=['GET'])
def get_sensor():
    sensors = Sensors.query.all()

    response = json.dumps([sens.as_dict() for sens in sensors], default=str)

    return response, 200
