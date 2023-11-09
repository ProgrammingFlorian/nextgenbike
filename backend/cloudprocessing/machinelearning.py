import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import TensorDataset, DataLoader
from torch import optim
import numpy as np

import backend.config as config
import dataprocessing as dp
import surfacemodelclass as sf
import util


def gen_dataloader(x, y, test_size=0.1, random_state=0):
    scaler = MinMaxScaler()  # TODO: choose scaler
    scaler.fit(x)
    x = scaler.transform(x)

    x = torch.tensor(x)
    y = torch.tensor(y)

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=test_size, random_state=random_state)

    train_x = torch.Tensor(train_x)
    train_y = F.one_hot(train_y.long(), len(config.classes)).to(torch.float32)

    test_x = torch.Tensor(test_x)
    test_y = F.one_hot(test_y.long(), len(config.classes)).to(torch.float32)

    train_dataset = TensorDataset(train_x, train_y)
    test_dataset = TensorDataset(test_x, test_y)

    train_loader = DataLoader(train_dataset)
    test_loader = DataLoader(test_dataset)

    return train_loader, test_loader


def train_model(model, train_loader):
    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

    print("Training STARTED")

    for e in range(0, config.num_training_epochs):
        model.train()  # set the model in training mode
        total_train_loss = 0  # initialize the total training and validation loss

        for i, (training_input, target) in enumerate(train_loader):  # loop over the training set
            hidden = model.initHidden()
            model.zero_grad()

            output = [.0, .0, .0, .0]
            for data_row in training_input:
                for i in range(0, len(data_row), config.n_training_cols):
                    model_input = data_row[None, i:i + config.n_training_cols].float()
                    output, hidden = model(model_input, hidden)

            optimizer.zero_grad()
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            # add the loss to the total training loss so far and calculate the number of correct predictions
            total_train_loss += loss.item()

        if (e + 1) % 10 == 0:
            print("Epoch", e + 1, "Training Loss:", total_train_loss)

    print("Training FINISHED")

    return model, criterion


def print_training_accuracy(model, train_loader, criterion):
    training_loss, class_correct, class_total = util.compute_accuracy(model=model, loader=train_loader, criterion=criterion)

    # average training loss
    training_loss = training_loss / len(train_loader.dataset)
    print('Training Loss: {:.6f}\n'.format(training_loss))
    for i in range(len(config.classes)):
        if class_total[i] > 0:
            print('Training Accuracy of %5s: %2d%% (%2d/%2d)' % (
                config.classes[i], 100.0 * class_correct[i] / class_total[i],
                np.sum(class_correct[i]), np.sum(class_total[i])))
        else:
            print('Training Accuracy of %5s: N/A ' % (config.classes[i]))

    print('Training Accuracy (Overall): %2d%% (%2d/%2d)' % (
        100. * np.sum(class_correct) / np.sum(class_total),
        np.sum(class_correct), np.sum(class_total)))


def print_testing_accuracy(model, test_loader, criterion):
    test_loss, class_correct, class_total = util.compute_accuracy(model=model, loader=test_loader, criterion=criterion)

    # average test loss
    test_loss = test_loss / len(test_loader.dataset)
    print('Test Loss: {:.6f}\n'.format(test_loss))

    for i in range(len(config.classes)):
        if class_total[i] > 0:
            print('Test Accuracy of %5s: %2d%% (%2d/%2d)' % (
                config.classes[i], 100.0 * class_correct[i] / class_total[i],
                np.sum(class_correct[i]), np.sum(class_total[i])))
        else:
            print('Test Accuracy of %5s: N/A (no testing examples)' % (config.classes[i]))

    print('\nTest Accuracy (Overall): %2d%% (%2d/%2d)' % (
        100. * np.sum(class_correct) / np.sum(class_total),
        np.sum(class_correct), np.sum(class_total)))


def start_ml(json_data):
    if json_data is None:
        json_data = dp.get_data_db()

    X, Y = dp.data_preparation(json_data)
    train_loader, test_loader = gen_dataloader(X, Y)
    model = sf.RNN(config.n_training_cols, config.n_hidden_layers, len(config.classes))
    model, criterion = train_model(model=model, train_loader=train_loader)

    print_training_accuracy(model=model, train_loader=train_loader, criterion=criterion)
    print_testing_accuracy(model=model, test_loader=test_loader, criterion=criterion)
