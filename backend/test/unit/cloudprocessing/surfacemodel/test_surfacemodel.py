import os
import unittest.mock

import pytest

import cloudprocessing.surfacemodel.config as sf_config
import cloudprocessing.surfacemodel.surfacemodel as sf
from test.unit.cloudprocessing.surfacemodel import (single_element_dataframe_no_terrain, single_element_data_asphalt,
                                                    single_element_data_long_asphalt, test_dataframe)


def test_group_trip_second_no_terrain(single_element_dataframe_no_terrain):
    grouped = sf.group_trip_second(single_element_dataframe_no_terrain)

    assert grouped is None


@pytest.mark.parametrize("example_dataframe", [
    single_element_data_asphalt(), single_element_data_long_asphalt(), test_dataframe()
])
def test_data_preparation_norm_len(example_dataframe):
    x, y = sf.data_preparation(example_dataframe)

    assert len(x) == len(y) == 1
    assert len(x[0]) == sf_config.batch_size * sf_config.n_training_cols


@pytest.mark.parametrize("example_dataframe", [
    single_element_data_asphalt(), single_element_data_long_asphalt(), test_dataframe()
])
@unittest.mock.patch('cloudprocessing.surfacemodel.surfacemodel.torch.save')
def test_sf_runs(torch_save, example_dataframe):
    sf.initiate(example_dataframe)

    torch_save.assert_called_once()
    assert not os.path.exists(sf_config.surfacemodel_path)
