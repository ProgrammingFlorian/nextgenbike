import pandas as pd

from cloudprocessing.surfacemodel.config import batch_size


def single_element_dataframe_string(terrain_string):
    return ('[{"time": "2023-01-01 12:00:00.00", "trip_id": 0, "vibration": 0, "latitude": 0.0, '
            '"longitude": 0.0, "acceleration_x": 0, "acceleration_y": 0, "acceleration_z": 0, '
            '"gyroscope_x": 0, "gyroscope_y": 0, "gyroscope_z": 0, '
            '"crash": null, "terrain": ' + terrain_string + '}]')


def single_element_dataframe(terrain_string):
    df = pd.read_json(single_element_dataframe_string(terrain_string))
    df['time'] = pd.to_datetime(df['time'], format='mixed')
    return df


def single_element_data_long_asphalt():
    df = single_element_dataframe("0")
    dataframe = pd.DataFrame()

    for i in range(batch_size * 2):
        dataframe = pd.concat([dataframe, df])

    return dataframe
