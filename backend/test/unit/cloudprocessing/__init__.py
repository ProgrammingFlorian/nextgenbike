import pytest

from server.server import rnn
from server.server import config as sf_config


@pytest.fixture
def example_sf_rnn():
    return rnn.RNN(sf_config.n_training_cols, sf_config.n_hidden_layers, len(sf_config.classes))