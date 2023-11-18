from server.server import config as sf_config
from test.unit.cloudprocessing import example_sf_rnn


def test_correct_init(example_sf_rnn):
    assert example_sf_rnn.hidden_size == sf_config.n_hidden_layers

    assert example_sf_rnn.i2h.in_features == sf_config.n_training_cols + sf_config.n_hidden_layers
    assert example_sf_rnn.i2h.out_features == sf_config.n_hidden_layers

    assert example_sf_rnn.h2o.in_features == sf_config.n_hidden_layers
    assert example_sf_rnn.h2o.out_features == len(sf_config.classes)
