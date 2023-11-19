import datetime
import os
from unittest import mock

import pandas as pd
import pandas.testing
from freezegun import freeze_time

import machinelearning as ml
import test
from test.unit.cloudprocessing.surfacemodel import single_element_dataframe_string, test_dataframe_string, \
    test_dataframe


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


ospathexists = os.path.exists


def mock_file_exists(file):
    global ospathexists
    if file == "surfacemodel/test_model_path":
        return True
    else:
        return ospathexists(file)


@mock.patch("machinelearning.config.surfacemodel_path", "test_model_path")
@mock.patch("machinelearning.os.path.exists", side_effect=mock_file_exists)
@mock.patch("machinelearning.sf.continue_training", return_value="return")
def test_start_ml(continue_training, exists):
    test_dataframe()
    json = test_dataframe_string()
    result = ml.start_ml(json)

    assert result == "return"
    exists.assert_called_with("surfacemodel/test_model_path")

    pandas.testing.assert_frame_equal(continue_training.call_args[0][0], pd.read_json(json))



@mock.patch("machinelearning.last_time_pred", test.test_date)
@freeze_time(test.test_date.__add__(datetime.timedelta(seconds=2)))
@mock.patch("machinelearning.predict_on_data")
def test_try_to_predict_none(predict_on_data):
    ml.try_to_predict()

    assert not predict_on_data.called


def test_predict_no_data():
    prediction = ml.predict_on_data("{}")

    assert prediction == []


@mock.patch("machinelearning.sf.predict_df", return_value="return_value")
def test_predict(predict_df):
    json = single_element_dataframe_string("null")
    result = ml.predict_on_data(json)
    assert result == "return_value"

    pandas.testing.assert_frame_equal(predict_df.call_args[0][0], pd.read_json(json))
