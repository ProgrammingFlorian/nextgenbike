import json

from flask import request, Blueprint
from marshmallow import Schema, ValidationError, fields

from app import database_functions as dbf
import app.utils as utils
import machinelearning as ml

url = Blueprint('urls', __name__)


class CreateUserSchema(Schema):
    username = fields.String(required=True)


class TripStartSchema(Schema):
    name = fields.String(required=True)
    user_id = fields.Integer(required=True)


class TripIdSchema(Schema):
    trip_id = fields.Integer(required=False)


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
    return 'Welcome to the Next-Gen Bike backend!'


@url.route('/users', methods=['GET'])
def get_users():
    users = dbf.get_all_users()
    return utils.dict_array_as_json(users), 200


@url.route('/users', methods=['POST'])
def create_user():
    schema = CreateUserSchema()
    try:
        request_data = schema.load(request.json)
    except ValidationError as err:
        print(f"ValidationError {err}")
        return json.dumps(err.messages), 400
    print(f"Received request with payload {request_data}")

    user = dbf.create_user(request_data['username'])
    response = json.dumps({"user_id": user.id})

    return response, 200


@url.route('/trip/start', methods=['POST'])
def trip_start():
    schema = TripStartSchema()
    try:
        request_data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {request_data}")

    trip = dbf.create_trip(request_data['name'], request_data['user_id'])
    response = json.dumps({"trip_id": trip.id})

    return response, 200


@url.route('/trip/end', methods=['POST'])
def trip_end():
    schema = TripIdSchema()
    try:
        request_data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {request_data}")

    trip = dbf.end_trip(request_data['trip_id'])
    response = json.dumps({"status": "success", "trip_id": trip.id, "trip_end": trip.end}, default=str)

    return response, 200


@url.route('/trips', methods=['GET'])
def get_trips():
    trips = dbf.get_trip_data()
    return utils.dict_array_as_json(trips), 200


@url.route('/sensor', methods=['PUT'])
def put_sensor_data():
    schema = SensorSchema()
    try:
        request_data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {request_data}")

    dbf.put_sensor_data(request_data)

    print("trying to predict..")
    ml.try_to_predict()
    print("done")
    # pred_process = Process(target=ml.try_to_predict, daemon=True)
    # pred_process.start()

    return json.dumps({"status": "success"}), 200


@url.route('/sensor', methods=['GET'])
def get_sensor():
    sensors = dbf.get_sensor_data()
    return utils.dict_array_as_json(sensors), 200


@url.route('/terrain', methods=['POST'])
def get_terrain():
    schema = TripIdSchema()
    try:
        request_data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {request_data}")

    if 'trip_id' not in request_data:
        terrain = dbf.get_terrain_data()
    else:
        terrain = dbf.get_terrain_data_by_trip_id(request_data['trip_id'])

    return terrain, 200


@url.route('/retrain', methods=['POST'])
def retrain():
    sensors = dbf.get_sensor_data()
    sensors_json = utils.dict_array_as_json(sensors)
    ml.start_ml(sensors_json)

    return json.dumps({"status": "success", "message": "started retraining the model"}), 200
