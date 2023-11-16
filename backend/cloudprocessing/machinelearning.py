import pandas as pd

import dataprocessing as dp




def start_ml(json_data):
    dataframe = dp.pre_processing(pd.read_json(json_data))



