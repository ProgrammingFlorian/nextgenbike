import pytest

from server.cloudprocessing import rnn
from server.cloudprocessing.surfacemodel import config as sf_config


@pytest.fixture
def example_sf_rnn():
    return rnn.RNN(sf_config.n_training_cols, sf_config.n_hidden_layers, len(sf_config.classes))


def example_predict_input():
    return