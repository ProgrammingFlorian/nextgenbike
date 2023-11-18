import pandas as pd
import pytest

from server.cloudprocessing import config

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

    long_dataframe = pd.DataFrame(columns=config.preprocessed_columns, )

    return long_dataframe
