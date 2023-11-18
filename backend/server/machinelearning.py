import pandas as pd
import os

import server.cloudprocessing.surfacemodel.surfacemodel as sf
from server.cloudprocessing.surfacemodel import config as config


def initiate_ml(dataframe):
    sf.initiate(dataframe)


def start_ml(json_data):
    dataframe = pd.read_json(json_data)
    if not os.path.exists("surfacemodel/" + config.surfacemodel_path):
        return initiate_ml(dataframe)

    return sf.continue_training(dataframe)


def predict_on_data(json_data) -> list:
    df = pd.read_json(json_data)
    if df.empty:
        return []
    else:
        return sf.predict_df(pd.read_json(json_data))
