import json
from datetime import datetime

from flask import request, Blueprint

from app.extensions import db
from app.models import Trip, Vibration, GPS, IMU

url = Blueprint('urls', __name__)


@url.route('/')
@url.route('/index')
def index():
    return 'Hello, World!'


@url.route('/sensor', methods=['PUT'])
def sensor():
    data = json.loads(request.data)

    v = Vibration(data['vibration'], data['trip_id'])
    gps = GPS(data['latitude'], data['longitude'], data['trip_id'])
    imu = IMU(data['acceleration_x'], data['acceleration_y'], data['acceleration_z'], data['gyroscope_x'],
              data['gyroscope_y'], data['gyroscope_z'], data['trip_id'])

    db.session.add(v)
    db.session.add(gps)
    db.session.add(imu)
    db.session.commit()

    return 'Data submitted'


@url.route('/trip/start', methods=['POST'])
def trip_start():
    data = json.loads(request.data)

    trip = Trip(name=data['name'], user_id=data['user_id'])
    db.session.add(trip)
    db.session.commit()

    return 'New trip created'


@url.route('/trip/end', methods=['POST'])
def trip_end():
    data = json.loads(request.data)

    trip = db.session.execute(db.select(Trip).filter_by(id=data['trip_id'])).scalar_one()
    trip.end = datetime.utcnow()

    db.session.commit()

    return 'Trip finished'
