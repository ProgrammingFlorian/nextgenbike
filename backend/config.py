classes = ['asphalt', 'pavement', 'gravel', 'dirt']
learning_rate = 1e-3
momentum = 0.9
num_training_epochs = 30
batch_size = 10
n_training_cols = 8
n_hidden_layers = 64  # TODO maybe increase with more data


def map_to_int(c):
    for i, e in enumerate(classes):
        if c == e:
            return i


def map_to_string(i):
    return classes[i]
