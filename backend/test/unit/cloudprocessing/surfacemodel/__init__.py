import pandas as pd
import pytest

from cloudprocessing.surfacemodel.config import batch_size


@pytest.fixture
def single_element_dataframe_no_terrain():
    df = pd.read_json(('[{"time": "2023-01-01 12:00:00.00", "trip_id": 0, "vibration": 0, "latitude": 0.0, '
                       '"longitude": 0.0, "acceleration_x": 0, "acceleration_y": 0, "acceleration_z": 0, '
                       '"gyroscope_x": 0, "gyroscope_y": 0, "gyroscope_z": 0, '
                       '"crash": null, "terrain": null}]'))
    df['time'] = pd.to_datetime(df['time'], format='mixed')
    return df


def single_element_data_asphalt():
    df = pd.read_json(('[{"time": "2023-01-01 12:00:00.00", "trip_id": 0, "vibration": 0, "latitude": 0.0, '
                       '"longitude": 0.0, "acceleration_x": 0, "acceleration_y": 0, "acceleration_z": 0, '
                       '"gyroscope_x": 0, "gyroscope_y": 0, "gyroscope_z": 0, '
                       '"crash": null, "terrain": 0}]'))
    df['time'] = pd.to_datetime(df['time'], format='mixed')
    return df


def single_element_data_long_asphalt():
    df = single_element_data_asphalt()
    dataframe = pd.DataFrame()

    for i in range(batch_size * 2):
        dataframe = pd.concat([dataframe, df])

    return dataframe


def test_dataframe():
    return pd.read_json(
        '[{"time": "2023-11-05 17:35:18.484000", "trip_id": 0, "vibration": 0, "latitude": 0.0, "longitude": 0.0, '
        '"acceleration_x": 260.0, "acceleration_y": 15.0, "acceleration_z": -53.0, "gyroscope_x": 51.0, '
        '"gyroscope_y": 54.0, "gyroscope_z": 21.0, "crash": null, "terrain": 1}, '
        '{"time": "2023-11-05 17:35:18.537000", "trip_id": 0, "vibration": 0, "latitude": 0.0, "longitude": 0.0, '
        '"acceleration_x": 259.0, "acceleration_y": 13.0, "acceleration_z": -56.0, "gyroscope_x": 16.0, '
        '"gyroscope_y": 22.0, "gyroscope_z": 208.0, "crash": null, "terrain": 2}, {"time": '
        '"2023-11-05 17:35:18.589000", "trip_id": 0, "vibration": 0, "latitude": 0.0, "longitude": '
        '0.0, "acceleration_x": 262.0, "acceleration_y": 6.0, "acceleration_z": -57.0, "gyroscope_x": -20.0, '
        '"gyroscope_y": 78.0, "gyroscope_z": -76.0, "crash": null, "terrain": 2}, {"time": '
        '"2023-11-05 17:35:18.641000", "trip_id": 0, "vibration": 0, "latitude": 0.0, "longitude": 0.0, '
        '"acceleration_x": 255.0, "acceleration_y": 8.0, "acceleration_z": -54.0, "gyroscope_x": 1.0, '
        '"gyroscope_y": -11.0, "gyroscope_z": 4.0, "crash": null, "terrain": 3}, {"time": "2023-11-05 '
        '17:35:24.245000", "trip_id": 0, "vibration": 0, "latitude": 0.0, "longitude": 0.0, "acceleration_x": '
        '258.0, "acceleration_y": 9.0, "acceleration_z": -58.0, "gyroscope_x": -10.0, "gyroscope_y": 64.0, '
        '"gyroscope_z": -4.0, "crash": null, "terrain": 1}, {"time": "2023-11-05 17:35:24.297000", '
        '"trip_id": 0, "vibration": 0, "latitude": 0.0, "longitude": 0.0, "acceleration_x": 258.0, '
        '"acceleration_y": 7.0, "acceleration_z": -57.0, "gyroscope_x": -10.0, "gyroscope_y": 66.0, "gyroscope_z": '
        '-6.0, "crash": null, "terrain": 0}]')
