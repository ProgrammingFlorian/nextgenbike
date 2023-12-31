from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset, DataLoader

import cloudprocessing.rnn as rnn
import cloudprocessing.surfacemodel.config as sf_config
import cloudprocessing.util as util
from cloudprocessing import dataprocessing as dp


def group_trip_second(df: DataFrame):
    df['time_second'] = df['time'].map(lambda x: pd.Timestamp(x).floor(freq='S'))
    df['time'] = df['time'].map(pd.Timestamp.timestamp)

    return df.groupby([df.trip_id, df.time_second])


def normalize_to_batch_length(df: DataFrame, length):
    if len(df.columns) != sf_config.n_training_cols:
        raise Exception("Wrong number of input columns (should be)", sf_config.n_training_cols,
                        ", please check data.\n"
                        "But input was: ", df)

    array = df.to_numpy().flatten()
    datacheck = [0, 0, 0]

    if len(array) == length:
        datacheck[0] = 1
    elif len(array) > length:
        datacheck[1] = 1
    else:
        datacheck[2] = 1
        fake_array = [1] * (length - len(array))
        array = np.append(array, fake_array)
    array = array[:length].flatten()

    return array, datacheck


def data_preparation(df: DataFrame):
    df.dropna(subset=['terrain'], inplace=True)
    if df.size == 0:
        raise Exception("No target values (terrain) in DataFrame found")
    grouped = group_trip_second(df)

    x, y = [], []

    data_checking = [0, 0, 0]
    total_trip_seconds, actual_length = len(grouped), 0

    for i, (trip_seconds, table) in enumerate(grouped):
        actual_length += len(table)

        train_input = table.drop(columns=['terrain', 'trip_id', 'crash', 'time_second', 'latitude', 'longitude'])
        train_input, d_check = normalize_to_batch_length(train_input, sf_config.batch_size * sf_config.n_training_cols)
        x.append(train_input)
        data_checking = np.add(data_checking, d_check)

        train_target = table.terrain.min()
        y.append(train_target)

    for i in range(len(sf_config.data_errors)):
        print(sf_config.data_errors[i], ": ", data_checking[i])
    print('Mean Frequency is: %f Hz' % (actual_length / total_trip_seconds))

    return np.array(x), np.array(y)


def gen_dataloader(x, y, test_size=0.2, random_state=0):
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    x = torch.tensor(x)
    y = torch.tensor(y)

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=test_size, random_state=random_state)

    train_x = torch.Tensor(train_x)
    train_y = F.one_hot(train_y.long(), len(sf_config.classes)).to(torch.float32)

    test_x = torch.Tensor(test_x)
    test_y = F.one_hot(test_y.long(), len(sf_config.classes)).to(torch.float32)

    train_dataset = TensorDataset(train_x, train_y)
    test_dataset = TensorDataset(test_x, test_y)

    train_loader = DataLoader(train_dataset)
    test_loader = DataLoader(test_dataset)

    return train_loader, test_loader


def train_model(model, train_loader, num_epochs=sf_config.num_training_epochs, lr=sf_config.learning_rate):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    print("Training STARTED")

    for e in range(0, num_epochs):
        model.train()  # set the model in training mode
        total_train_loss = 0  # initialize the total training and validation loss

        for i, (training_input, target) in enumerate(train_loader):  # loop over the training set
            model.zero_grad()

            output = util.predict(model, training_input)

            optimizer.zero_grad()
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            # add the loss to the total training loss so far and calculate the number of correct predictions
            total_train_loss += loss.item()

        if (e + 1) % 10 == 0:
            print("Epoch", e + 1, "Training Loss:", total_train_loss)

    print("Training FINISHED")

    torch.save(model.state_dict(), sf_config.surfacemodel_path)

    return model, criterion


def print_training_accuracy(model, train_loader, criterion, classes):
    training_loss, class_correct, class_total = util.compute_accuracy_rnn(model=model, loader=train_loader,
                                                                          criterion=criterion)

    # average training loss
    training_loss = training_loss / len(train_loader.dataset)
    print('Training Loss: {:.6f}\n'.format(training_loss))
    for i in range(len(classes)):
        if class_total[i] > 0:
            print('Training Accuracy of %5s: %2d%% (%2d/%2d)' % (
                classes[i], 100.0 * class_correct[i] / class_total[i],
                np.sum(class_correct[i]), np.sum(class_total[i])))
        else:
            print('Training Accuracy of %5s: N/A ' % (classes[i]))

    print('Training Accuracy (Overall): %2d%% (%2d/%2d)' % (
        100. * np.sum(class_correct) / np.sum(class_total),
        np.sum(class_correct), np.sum(class_total)))


def print_testing_accuracy(model, test_loader, classes, criterion):
    test_loss, class_correct, class_total = util.compute_accuracy_rnn(model=model, loader=test_loader,
                                                                      criterion=criterion)

    # average test loss
    test_loss = test_loss / len(test_loader.dataset)
    print('Test Loss: {:.6f}\n'.format(test_loss))

    for i in range(len(classes)):
        if class_total[i] > 0:
            print('Test Accuracy of %5s: %2d%% (%2d/%2d)' % (
                classes[i], 100.0 * class_correct[i] / class_total[i],
                np.sum(class_correct[i]), np.sum(class_total[i])))
        else:
            print('Test Accuracy of %5s: N/A (no testing examples)' % (classes[i]))

    print('\nTest Accuracy (Overall): %2d%% (%2d/%2d)' % (
        100. * np.sum(class_correct) / np.sum(class_total),
        np.sum(class_correct), np.sum(class_total)))


def train(model, dataframe):
    dataframe = dp.pre_processing(dataframe)
    x, y = data_preparation(dataframe)
    train_loader, test_loader = gen_dataloader(x, y)
    model, criterion = train_model(model=model, train_loader=train_loader)
    print_training_accuracy(model=model, train_loader=train_loader, criterion=criterion, classes=sf_config.classes)
    print_testing_accuracy(model=model, test_loader=test_loader, criterion=criterion, classes=sf_config.classes)


def predict_data_preparation(df):
    grouped = group_trip_second(df)

    data_checking = [0, 0, 0]
    total_trip_seconds, actual_length = len(grouped), 0

    x = []
    id_list, time_list, lat_list, lon_list = [], [], [], []

    for i, (trip_seconds, table) in enumerate(grouped):
        id_list.append(trip_seconds[0])
        time_list.append(trip_seconds[1])
        lat_list.append(table['latitude'].mean())
        lon_list.append(table['longitude'].mean())

        train_input = table.drop(columns=['terrain', 'trip_id', 'crash', 'time_second', 'latitude', 'longitude'])
        train_input, d_check = normalize_to_batch_length(train_input, sf_config.batch_size * sf_config.n_training_cols)
        x.append(train_input)
        data_checking = np.add(data_checking, d_check)

    for i in range(len(sf_config.data_errors)):
        print(sf_config.data_errors[i], ": ", data_checking[i])
    print('Mean Frequency is: %f Hz' % (actual_length / total_trip_seconds))

    return np.array(x), id_list, time_list, lat_list, lon_list


def predict_generate_data_loaders(x):
    x = torch.Tensor(torch.tensor(x))
    y = F.one_hot(torch.zeros(len(x)).long(), len(sf_config.classes)).to(torch.float32)
    dataset = TensorDataset(x, y)
    return DataLoader(dataset)


def predict_df(dataframe: DataFrame) -> list[dict[str, Any]]:
    dataframe = dp.format_time(dataframe)

    x, id_list, time_list, lat_list, lon_list = predict_data_preparation(dataframe)

    loader = predict_generate_data_loaders(x)

    model = rnn.RNN(sf_config.n_training_cols, sf_config.n_hidden_layers, len(sf_config.classes))
    model.load_state_dict(torch.load(sf_config.surfacemodel_path))

    terrain_guess = util.predict_dataset(model=model, x=loader)

    results = []
    for i in range(len(id_list)):
        results.append({"trip_id": id_list[i], "time": time_list[i], "latitude": lat_list[i], "longitude": lon_list[i],
                        "terrain": terrain_guess[i]})
    return results


def initiate(dataframe):
    if dataframe is None:
        dataframe = dp.get_dataframe()

    model = rnn.RNN(sf_config.n_training_cols, sf_config.n_hidden_layers, len(sf_config.classes))
    train(model, dataframe)


def continue_training(dataframe):
    model = rnn.RNN(sf_config.n_training_cols, sf_config.n_hidden_layers, len(sf_config.classes))
    model.load_state_dict(torch.load(sf_config.surfacemodel_path))
    train(model, dataframe)


if __name__ == '__main__':
    initiate(None)
