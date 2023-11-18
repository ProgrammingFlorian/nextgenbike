import pytest

import cloudprocessing.surfacemodel.config as sf_config

import cloudprocessing.surfacemodel.surfacemodel as sf
from test.unit.cloudprocessing.surfacemodel import (single_element_dataframe_no_terrain, single_element_data_asphalt,
                                                    single_element_data_long_asphalt)


def test_group_trip_second_no_terrain(single_element_dataframe_no_terrain):
    grouped = sf.group_trip_second(single_element_dataframe_no_terrain)

    assert grouped is None


@pytest.mark.parametrize("single_element_df", [
    single_element_data_asphalt(), single_element_data_long_asphalt()
])
def test_data_preparation_norm_len(single_element_df):
    x, y = sf.data_preparation(single_element_df)

    assert len(x) == len(y) == 1
    assert len(x[0]) == sf_config.batch_size * sf_config.n_training_cols
