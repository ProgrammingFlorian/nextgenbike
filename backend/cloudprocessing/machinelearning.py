import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

import surfacemodelclass as sf


def start_ml(data):
    dataset = pd.DataFrame(data)


def data_preparation(dataset, test_size, random_state):
    train_x, test_x, train_y, test_y = train_test_split(dataset.data, dataset.target, test_size=test_size, random_state=random_state)

    train_dataset = TensorDataset(train_x, train_y)
    test_dataset = TensorDataset(test_x, test_y)

    train_loader = DataLoader(train_dataset)

    test_loader = DataLoader(test_dataset)
    return train_loader, test_loader


def train_model(input_size, output_size, hidden_dim, n_layers, num_epochs, lr, momentum):
    model = sf.SurfaceModel(input_size, output_size, hidden_dim, n_layers)

    return model


def test_model_training_data(model, train_loader):
    print("x")
