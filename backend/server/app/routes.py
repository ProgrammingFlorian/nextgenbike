import json
import datetime

from multiprocessing import Process

from sqlalchemy import func, and_
from app.extensions import db
from app.models import User, Trip, Sensors, Terrain
from flask import request, Blueprint
from marshmallow import Schema, ValidationError, fields
import machinelearning as ml
from cloudprocessing import dataprocessing

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


@url.route('/users', methods=['GET'])
def get_user():
    data = User.query.all()

    response = json.dumps([d.as_dict() for d in data], default=str)

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
    schema = TripIdSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400
    print(f"Received request with payload {data}")

    trip = db.session.execute(db.select(Trip).filter_by(id=data['trip_id'])).scalar_one()
    trip.end = datetime.datetime.utcnow()

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

    # pred_process = Process(target=pred, daemon=True)
    # pred_process.start()
    pred()

    return 'Submitted sensor data', 200


last_time_pred = datetime.datetime.now().replace(microsecond=0)


def pred():
    global last_time_pred
    current_time = datetime.datetime.now().replace(microsecond=0)
    relevant_time_ago = current_time - datetime.timedelta(seconds=5)
    if last_time_pred < relevant_time_ago or True:
        last_time_pred = datetime.datetime.now()

        # data = Sensors.query.filter(and_(Sensors.time > relevant_time_ago, Sensors.time < current_time)).all()
        data = Sensors.query.all()
        data_json = json.dumps([d.as_dict() for d in data], default=str)
        print(data_json)
        results = ml.predict_on_data(data_json)
        for result in results:
            r = Terrain(result['time'], result['trip_id'], result['latitude'], result['longitude'],
                        result['terrain'])
            db.session.add(r)
        db.session.commit()


@url.route('/sensor', methods=['GET'])
def get_sensor():
    sensors = Sensors.query.all()

    response = json.dumps([sens.as_dict() for sens in sensors], default=str)

    return response, 200


@url.route('/trips', methods=['GET'])
def get_trips():
    data = Trip.query.all()

    response = json.dumps([d.as_dict() for d in data], default=str)

    return response, 200


@url.route('/terrain', methods=['POST'])
def get_terrain():
    schema = TripIdSchema()
    try:
        request_data = schema.load(request.json)
    except ValidationError as err:
        return json.dumps(err.messages), 400

    if 'trip_id' not in request_data:
        data = (Terrain.query.with_entities(Terrain.latitude, Terrain.longitude,
                                            func.min(Terrain.terrain).label('terrain'))
                .group_by(Terrain.latitude, Terrain.longitude)
                .order_by(Terrain.time.asc())).all()

    else:
        data = (Terrain.query.with_entities(Terrain.latitude, Terrain.longitude,
                                            func.min(Terrain.terrain).label('terrain'))
                .group_by(Terrain.latitude, Terrain.longitude)
                .filter_by(trip_id=request_data['trip_id'])
                .order_by(Terrain.time.asc())).all()

    response = []
    for d in data:
        response.append({"latitude": d[0], "longitude": d[1], "terrain": d[2]})

    return response, 200


@url.route('/retrain', methods=['POST'])
def retrain():
    data = Sensors.query.all()
    data_json = json.dumps([d.as_dict() for d in data], default=str)
    ml.start_ml(data_json)

    return "Started retraining model", 200


@url.route('/sql', methods=['GET'])
def sql():
    dataframe = dataprocessing.pre_processing(dataprocessing.get_dataframe())
    dataframe.dropna(subset=['terrain'], inplace=True)
    for i, row in dataframe.iterrows():
        _time = dataframe.loc[i, 'time']
        _trip_id = dataframe.loc[i, 'trip_id']
        _latitude = dataframe.loc[i, 'latitude']
        _longitude = dataframe.loc[i, 'longitude']
        _terrain = dataframe.loc[i, 'terrain']
        print(_trip_id)
        print(_latitude)
        print(_longitude)
        print(type(_time))
        print(_time.to_pydatetime())
        t = Terrain(_time.to_pydatetime(), _trip_id, _latitude, _longitude, _terrain)
        db.session.add(t)
    db.session.commit()

    return "done", 200
