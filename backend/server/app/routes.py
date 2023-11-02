import json
from datetime import datetime

from app.extensions import db
from app.models import Trip, Vibration, GPS, IMU, User
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
        return json.dumps(err.messages), 400

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

    v = Vibration(data['vibration'], data['trip_id'])
    gps = GPS(data['latitude'], data['longitude'], data['trip_id'])
    imu = IMU(data['acceleration_x'], data['acceleration_y'], data['acceleration_z'], data['gyroscope_x'],
              data['gyroscope_y'], data['gyroscope_z'], data['trip_id'])

    db.session.add(v)
    db.session.add(gps)
    db.session.add(imu)
    db.session.commit()

    return 'Submitted sensor data', 200
