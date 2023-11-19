import datetime
from unittest import mock

import pandas as pd
from freezegun import freeze_time

import machinelearning as ml
import test
from test.unit.cloudprocessing.surfacemodel import single_element_dataframe_string


@mock.patch("machinelearning.sf.initiate")
def test_initiate_ml(initiate):
    ml.initiate_ml("dataframe")

    initiate.assert_called_with("dataframe")


@mock.patch("machinelearning.config.surfacemodel_path", return_value="surfacemodel")
@mock.patch("machinelearning.os.path.exists", return_value=True)
@mock.patch("machinelearning.initiate_ml", return_value="return")
def test_start_ml(initiate_ml, exists, surfacemodel_path):
    json = single_element_dataframe_string("null")
    result = ml.start_ml(json)

    assert result == "return"
    exists.assert_called_with("surfacemodel/surfacemodel")
    surfacemodel_path.assert_called_with()

    initiate_ml.assert_called_with(pd.read_json(json))


@mock.patch("machinelearning.config.surfacemodel_path", return_value="test_model_path")
@mock.patch("machinelearning.os.path.exists", return_value=True)
@mock.patch("machinelearning.sf.continue_training", return_value="return")
def test_start_ml(continue_training, exists, surfacemodel_path):
    json = single_element_dataframe_string("null")
    result = ml.start_ml(json)

    assert result == "return"
    exists.assert_called_with("surfacemodel/test_model_path")
    surfacemodel_path.assert_called_with()

    continue_training.assert_called_with(pd.read_json(json))


@mock.patch("machinelearning.last_time_pred", return_value=test.test_date)
@freeze_time(test.test_date.__add__(datetime.timedelta(seconds=2)))
@mock.patch("machinelearning.predict_on_data")
def test_try_to_predict_none(predict_on_data, now):
    ml.try_to_predict()

    now.assert_called_with()
    assert not predict_on_data.called


def test_predict_no_data():
    prediction = ml.predict_on_data("{}")

    assert prediction == []


@mock.patch("machinelearning.sf.predict_df", return_value="return_value")
def test_predict(predict_df):
    json = single_element_dataframe_string("null")
    result = ml.predict_on_data(json)
    assert result == "return_value"

    predict_df.assert_called_with(pd.read_json(json))
