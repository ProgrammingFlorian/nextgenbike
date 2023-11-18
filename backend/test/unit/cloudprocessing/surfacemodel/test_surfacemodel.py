import pytest

import server.cloudprocessing.surfacemodel.config as sf_config

import server.cloudprocessing.surfacemodel.surfacemodel as sf
from test.unit.cloudprocessing.surfacemodel import (single_element_dataframe_no_terrain, single_element_data_asphalt,
                                                    single_element_data_long_asphalt)


def test_data_preparation_drop_no_terrain(single_element_dataframe_no_terrain):
    x, y = sf.data_preparation(single_element_dataframe_no_terrain)

    assert len(x) == 0
    assert len(y) == 0


@pytest.mark.parametrize("single_element_df", [
    single_element_data_asphalt(), single_element_data_long_asphalt()
])
def test_data_preparation_norm_len(single_element_df):
    x, y = sf.data_preparation(single_element_df)

    assert len(x) == len(y) == 1
    assert len(x[0]) == sf_config.batch_size * sf_config.n_training_cols
