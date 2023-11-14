import numpy as np
import pandas as pd
import requests
from requests.exceptions import ChunkedEncodingError

import backend.config as config


def get_data_db():
    return requests.get('http://104.248.148.208/sensor', timeout=10).text


def get_dataframe():
    raw_data = ""
    while raw_data == "":
        try:
            raw_data = get_data_db()
        except ChunkedEncodingError:
            print("Couldn't get Data, retrying ...")

    return pd.read_json(raw_data)


def pre_processing(dataframe):
    # cycling session 06.11.2023
    pavement_start = pd.Timestamp(year=2023, month=11, day=6, hour=18, minute=33)
    pavement_end = pd.Timestamp(year=2023, month=11, day=6, hour=18, minute=55)
    asphalt_start_1 = pd.Timestamp(year=2023, month=11, day=6, hour=19, minute=9)
    asphalt_end_1 = pd.Timestamp(year=2023, month=11, day=6, hour=19, minute=17)
    asphalt_start_2 = pd.Timestamp(year=2023, month=11, day=6, hour=19, minute=31)
    asphalt_end_2 = pd.Timestamp(year=2023, month=11, day=6, hour=20, minute=00)

    # cycling session 09.11.2023
    asphalt_start_3 = pd.Timestamp(year=2023, month=11, day=9, hour=20, minute=20)
    asphalt_end_3 = pd.Timestamp(year=2023, month=11, day=9, hour=21, minute=0)
    pavement_start_2 = pd.Timestamp(year=2023, month=11, day=9, hour=21, minute=5)
    pavement_end_2 = pd.Timestamp(year=2023, month=11, day=9, hour=21, minute=30)

    # cycling session 13.11.2023
    grass_start = pd.Timestamp(year=2023, month=11, day=13, hour=20, minute=00)
    grass_end = pd.Timestamp(year=2023, month=11, day=13, hour=20, minute=20)

    # cycling session 14.11.2023
    grass_start_2 = pd.Timestamp(year=2023, month=11, day=14, hour=12, minute=23)
    grass_end_2 = pd.Timestamp(year=2023, month=11, day=14, hour=12, minute=44)
    asphalt_start_4 = pd.Timestamp(year=2023, month=11, day=14, hour=12, minute=52)
    asphalt_end_4 = pd.Timestamp(year=2023, month=11, day=14, hour=13, minute=15)

    # cycling session
    gravel_start = pd.Timestamp(year=3000, month=11, day=14, hour=12, minute=44)
    gravel_end = pd.Timestamp(year=3000, month=11, day=14, hour=12, minute=44)

    asphalt_count = 0
    pavement_count = 0
    gravel_count = 0
    grass_count = 0

    dataframe['time'] = pd.to_datetime(dataframe['time'], format='mixed')
    for i, row in dataframe.iterrows():
        if pavement_start <= row.time <= pavement_end or pavement_start_2 <= row.time <= pavement_end_2:
            dataframe.at[i, 'terrain'] = config.map_to_int('pavement')
            pavement_count += 1
        elif asphalt_start_1 <= row.time <= asphalt_end_1 or asphalt_start_2 <= row.time <= asphalt_end_2 or asphalt_start_3 <= row.time <= asphalt_end_3 or asphalt_start_4 <= row.time <= asphalt_end_4:
            dataframe.at[i, 'terrain'] = config.map_to_int('asphalt')
            asphalt_count += 1
        elif gravel_start <= row.time <= gravel_end:
            dataframe.at[i, 'terrain'] = config.map_to_int('gravel')
            gravel_count += 1
        elif grass_start <= row.time <= grass_end or grass_start_2 <= row.time <= grass_end_2:
            dataframe.at[i, 'terrain'] = config.map_to_int('grass')
            grass_count += 1

    print("Asphalt Data points: ", asphalt_count)
    print("Pavement Data points: ", pavement_count)
    print("Gravel Data points: ", gravel_count)
    print("Grass Data points: ", grass_count)

    return dataframe


def data_preparation(df):
    global n_cols

    df.dropna(subset=['terrain'], inplace=True)

    df['time_second'] = df.time.map(lambda x: pd.Timestamp(x).floor(freq='S'))
    df['time'] = df.time.map(pd.Timestamp.timestamp)

    grouped = df.groupby([df.trip_id, df.time_second])  # grouped.get_group(1)
    x = []
    y = []

    # data verification
    data_errors = ['GOOD', 'LONG', 'SHORT']
    data_checking = [0, 0, 0]
    total_samples = 0
    total_length = 0

    for i, (trip_seconds, table) in enumerate(grouped):
        if (i + 1) % 100 == 0:
            print("# trip seconds: " + str(i + 1))

        train_input = table.drop(columns=['terrain', 'trip_id', 'crash', 'time_second', 'latitude', 'longitude'])
        n_cols = len(train_input.columns)

        train_input = train_input.to_numpy()

        input_length = len(train_input)
        total_length += input_length
        if input_length == config.batch_size:
            data_checking[0] += 1
        elif input_length > config.batch_size:
            data_checking[1] += 1
            train_input = train_input[:config.batch_size]
        else:
            data_checking[2] += 1
            n_missing_rows = config.batch_size - len(train_input)
            for _ in range(n_missing_rows):
                fake_array = [1] * n_cols
                train_input = np.append(train_input, fake_array)

        train_target = table.terrain.min()

        x.append(train_input)
        y.append(train_target)
        total_samples += 1

    print('Printing Data Accuracy to ', config.batch_size, ' Hz frequency ...')
    for i in range(len(data_checking)):
        if total_samples > 0:
            print('%5s: %2d%% (%2d/%2d)' % (
                data_errors[i], 100.0 * data_checking[i] / total_samples,
                np.sum(data_checking[i]), total_samples))
        else:
            raise Exception("No Data Samples found, please check db connection")

    print('Mean Batch Length: %2.2f per Tripsecond ' % (total_length / total_samples))

    return np.array(x), np.array(y)
