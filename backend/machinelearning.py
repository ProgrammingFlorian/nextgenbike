import datetime

import pandas as pd
import os

from cloudprocessing.surfacemodel import config
from cloudprocessing.surfacemodel import surfacemodel as sf
import app.database_functions as dbf
import app.utils as utils


def initiate_ml(dataframe):
    sf.initiate(dataframe)


def start_ml(json_data):
    dataframe = pd.read_json(json_data)
    if not os.path.exists("surfacemodel/" + config.surfacemodel_path):
        return initiate_ml(dataframe)

    return sf.continue_training(dataframe)


last_time_pred = datetime.datetime.now().replace(microsecond=0)


def try_to_predict():
    global last_time_pred
    current_time = datetime.datetime.now().replace(microsecond=0)
    relevant_time_ago = current_time - datetime.timedelta(seconds=10)
    if last_time_pred < relevant_time_ago:
        last_time_pred = datetime.datetime.now()

        data = dbf.get_sensor_data_between(relevant_time_ago, current_time)
        data_json = utils.dict_array_as_json(data)

        predictions = predict_on_data(data_json)

        dbf.put_terrain_data(predictions)


def predict_on_data(json_data) -> list:
    df = pd.read_json(json_data)
    if df.empty:
        return []
    else:
        return sf.predict_df(df)
