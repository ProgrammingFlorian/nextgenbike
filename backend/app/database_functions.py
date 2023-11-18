import datetime

from sqlalchemy import and_, func

from app.extensions import db
from app.models import User, Trip, Sensors, Terrain


def create_user(username) -> User:
    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    return user


def get_all_users() -> [User]:
    return User.query.all()


def create_trip(name, user_id) -> Trip:
    trip = Trip(name=name, user_id=user_id)
    db.session.add(trip)
    db.session.commit()


def end_trip(trip_id) -> Trip:
    trip = db.session.execute(db.select(Trip).filter_by(id=trip_id)).scalar_one()
    trip.end = datetime.datetime.utcnow()

    db.session.commit()


def put_sensor_data(sensor_data):
    for i in range(len(sensor_data['time'])):
        sensor_row = Sensors(time=sensor_data['time'][i], trip_id=sensor_data['trip_id'],
                             vibration=sensor_data['vibration'][i],
                             latitude=sensor_data['latitude'][i], longitude=sensor_data['longitude'][i],
                             acceleration_x=sensor_data['acceleration_x'][i],
                             acceleration_y=sensor_data['acceleration_y'][i],
                             acceleration_z=sensor_data['acceleration_z'][i], gyroscope_x=sensor_data['gyroscope_x'][i],
                             gyroscope_y=sensor_data['gyroscope_y'][i], gyroscope_z=sensor_data['gyroscope_z'][i])
        db.session.add(sensor_row)
    db.session.commit()


def get_sensor_data_between(start, end):
    return Sensors.query.filter(and_(Sensors.time > start, Sensors.time < end)).all()


def put_terrain_data(terrain_data):
    for data in terrain_data:
        r = Terrain(data['time'], data['trip_id'], data['latitude'], data['longitude'],
                    data['terrain'])
        db.session.add(r)
    db.session.commit()


def get_sensor_data() -> [Sensors]:
    return Sensors.query.all()


def get_trip_data() -> [Trip]:
    return Trip.query.all()


def terrain_list_to_dict(terrain_list):
    terrain_dict = []
    for t in terrain_list:
        terrain_dict.append({"latitude": t[0], "longitude": t[1], "terrain": t[2]})

    return terrain_dict


def get_terrain_data() -> [Terrain]:
    terrain_list = (Terrain.query.with_entities(Terrain.latitude, Terrain.longitude,
                                                func.min(Terrain.terrain).label('terrain'))
                    .group_by(Terrain.latitude, Terrain.longitude)
                    .order_by(Terrain.time.asc())).all()
    return terrain_list_to_dict(terrain_list)


def get_terrain_data_by_trip_id(trip_id) -> [Terrain]:
    terrain_list = (Terrain.query.with_entities(Terrain.latitude, Terrain.longitude,
                                                func.min(Terrain.terrain).label('terrain'))
                    .group_by(Terrain.latitude, Terrain.longitude)
                    .filter_by(trip_id=trip_id)
                    .order_by(Terrain.time.asc())).all()

    return terrain_list_to_dict(terrain_list)
