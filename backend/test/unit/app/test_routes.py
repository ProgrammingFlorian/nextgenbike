import datetime
import unittest.mock as mock

import test
from app.models import User, Trip, Sensors
from test import test_date
from test.unit.app import client

dbf_get_all_users = [User(id=1, username="Peter"), User(id=2, username="Wei Chang"), User(id=3, username="Florian")]
dbf_create_user = User(id=1, username="Peter")

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@mock.patch("app.routes.dbf.get_all_users", return_value=dbf_get_all_users)
def test_get_users(get_all_users, client):
    result = client.get("/users")

    get_all_users.assert_called_with()

    json = result.data.decode()
    assert (json ==
            '[{"id": 1, "username": "Peter"}, {"id": 2, "username": "Wei Chang"}, {"id": 3, "username": "Florian"}]')


@mock.patch("app.routes.dbf.create_user", return_value=dbf_create_user)
def test_create_user(create_user, client):
    result = client.post("/users", data='{"username": "Peter"}', headers=headers)

    create_user.assert_called_with("Peter")

    json = result.data.decode()
    assert json == '{"user_id": 1}'


@mock.patch("app.routes.dbf.create_trip", return_value=Trip(name="test_trip", id=1))
def test_trip_start(create_trip, client):
    result = client.post("/trip/start", data='{"name": "test_trip", "user_id": 1}', headers=headers)

    create_trip.assert_called_with("test_trip", 1)

    json = result.data.decode()
    assert json == '{"trip_id": 1}'


@mock.patch("app.routes.dbf.end_trip",
            return_value=Trip(name="test_trip", id=1, end=test_date))
def test_trip_end(end_trip, client):
    result = client.post("/trip/end", data='{"trip_id": 1}', headers=headers)

    end_trip.assert_called_with(1)

    json = result.data.decode()
    assert json == '{"status": "success", "trip_id": 1, "trip_end": "2020-10-05 18:13:03"}'


@mock.patch("app.routes.dbf.get_trip_data",
            return_value=[
                Trip(id=1, start=test.test_date, end=datetime.datetime(2020, 10, 6, 1),
                     name="my first trip", user_id=1)])
def test_get_trips(get_trip_data, client):
    result = client.get("/trips")

    get_trip_data.assert_called_with()

    json = result.data.decode()
    assert json == ('[{"id": 1, "start": "2020-10-05 18:13:03", "end": "2020-10-06 01:00:00", "name": "my first trip", '
                    '"user_id": 1}]')


@mock.patch("app.routes.dbf.put_sensor_data")
@mock.patch("app.routes.ml.try_to_predict")
def test_put_sensor_data(try_to_predict, put_sensor_data, client):
    result = client.put("/sensor",
                        data='{"time": ["2014-12-22T03:12:58.019067+00:00", "2014-12-22T03:12:58.019057+00:00", '
                             '"2014-12-22T03:12:58.019047+00:00", "2014-12-22T03:12:58.019037+00:00"], "trip_id": 10, '
                             '"vibration": [1.0, 0.5, 2.0, 5.0], "latitude": [-5, -4.9, -4.8, -4.7], '
                             '"longitude": [1, 1.9, 2.8, 3.7], "acceleration_x": [1, 0, 5, 3], '
                             '"acceleration_y": [3, 8, 4, 1], "acceleration_z": [6, 3, 6, 2], '
                             '"gyroscope_x": [3, 2, 5, 3], "gyroscope_y": [7, 0, 2, 5], "gyroscope_z": [9, 1, 0, 8]}',
                        headers=headers)

    put_sensor_data.assert_called_with({'acceleration_x': [1.0, 0.0, 5.0, 3.0],
                                        'acceleration_y': [3.0, 8.0, 4.0, 1.0],
                                        'acceleration_z': [6.0, 3.0, 6.0, 2.0],
                                        'gyroscope_x': [3.0, 2.0, 5.0, 3.0],
                                        'gyroscope_y': [7.0, 0.0, 2.0, 5.0],
                                        'gyroscope_z': [9.0, 1.0, 0.0, 8.0],
                                        'latitude': [-5.0, -4.9, -4.8, -4.7],
                                        'longitude': [1.0, 1.9, 2.8, 3.7],
                                        'time': [datetime.datetime(2014, 12, 22, 3, 12, 58, 19067,
                                                                   tzinfo=datetime.timezone(datetime.timedelta(0),
                                                                                            '+0000')),
                                                 datetime.datetime(2014, 12, 22, 3, 12, 58, 19057,
                                                                   tzinfo=datetime.timezone(datetime.timedelta(0),
                                                                                            '+0000')),
                                                 datetime.datetime(2014, 12, 22, 3, 12, 58, 19047,
                                                                   tzinfo=datetime.timezone(datetime.timedelta(0),
                                                                                            '+0000')),
                                                 datetime.datetime(2014, 12, 22, 3, 12, 58, 19037,
                                                                   tzinfo=datetime.timezone(datetime.timedelta(0),
                                                                                            '+0000'))],
                                        'trip_id': 10,
                                        'vibration': [1.0, 0.5, 2.0, 5.0]}, )
    try_to_predict.assert_called_with()

    json = result.data.decode()
    assert json == '{"status": "success"}'


@mock.patch("app.routes.dbf.get_sensor_data",
            return_value=[Sensors(time=test.test_date, trip_id=1, vibration=1, latitude=5.0, longitude=3.3,
                                  acceleration_x=1.1, acceleration_y=2.2, acceleration_z=3.3, gyroscope_x=3.5,
                                  gyroscope_y=8.5,
                                  gyroscope_z=-134.5, crash=0, terrain=3)])
def test_get_sensor(get_sensor_data, client):
    result = client.get("/sensor")

    get_sensor_data.assert_called_with()

    json = result.data.decode()
    assert json == ('[{"time": "2020-10-05 18:13:03", "trip_id": 1, "vibration": 1, "latitude": 5.0, "longitude": 3.3, '
                    '"acceleration_x": 1.1, "acceleration_y": 2.2, "acceleration_z": 3.3, "gyroscope_x": 3.5, '
                    '"gyroscope_y": 8.5, "gyroscope_z": -134.5, "crash": 0, "terrain": 3}]')


@mock.patch("app.routes.dbf.get_terrain_data",
            return_value=[{'time': '2020-10-05 18:13:03', 'latitude': 1.303, 'longitude': 103.79, 'terrain': 1}])
def test_get_terrain(get_terrain_data, client):
    result = client.post("/terrain", data="{}", headers=headers)

    get_terrain_data.assert_called_with()

    json = result.data.decode()
    assert json == ('[{"latitude":1.303,"longitude":103.79,"terrain":1,"time":"2020-10-05 '
                    '18:13:03"}]\n')


@mock.patch("app.routes.dbf.get_terrain_data_by_trip_id",
            return_value=[{'time': '2020-10-05 18:13:03', 'latitude': 1.303, 'longitude': 103.79, 'terrain': 1}])
def test_get_terrain_with_trip_id(get_terrain_data_by_trip_id, client):
    result = client.post("/terrain", data='{"trip_id": 1}', headers=headers)

    get_terrain_data_by_trip_id.assert_called_with(1)

    json = result.data.decode()
    assert json == ('[{"latitude":1.303,"longitude":103.79,"terrain":1,"time":"2020-10-05 '
                    '18:13:03"}]\n')


@mock.patch("app.routes.dbf.get_sensor_data",
            return_value=[Sensors(time=test.test_date, trip_id=1, vibration=1, latitude=5.0, longitude=3.3,
                                  acceleration_x=1.1, acceleration_y=2.2, acceleration_z=3.3, gyroscope_x=3.5,
                                  gyroscope_y=8.5,
                                  gyroscope_z=-134.5, crash=0, terrain=3)])
@mock.patch("app.routes.ml.start_ml")
def test_retrain(start_ml, get_sensor_data, client):
    result = client.post("/retrain", headers=headers)

    get_sensor_data.assert_called_with()
    start_ml.assert_called_with('[{"time": "2020-10-05 18:13:03", "trip_id": 1, "vibration": 1, "latitude": '
                                '5.0, "longitude": 3.3, "acceleration_x": 1.1, "acceleration_y": 2.2, '
                                '"acceleration_z": 3.3, "gyroscope_x": 3.5, "gyroscope_y": 8.5, '
                                '"gyroscope_z": -134.5, "crash": 0, "terrain": 3}]')

    json = result.data.decode()
    assert json == '{"status": "success", "message": "started retraining the model"}'
