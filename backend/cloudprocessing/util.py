import torch

from cloudprocessing.surfacemodel import config as sf_config


def predict(model, pred_input) -> torch.Tensor:
    hidden = model.init_hidden()

    output = [.0, .0, .0, .0]
    for data_row in pred_input:
        for i in range(0, len(data_row), sf_config.n_training_cols):
            model_input = data_row[None, i:i + sf_config.n_training_cols].float()
            output, hidden = model(model_input, hidden)

    return output


def compute_accuracy_rnn(model, loader, criterion):
    loss = 0.0
    class_c, class_t = list(0. for _ in range(len(sf_config.classes))), list(0. for _ in range(len(sf_config.classes)))

    model.eval()
    for i, (pred_input, target) in enumerate(loader):
        output = predict(model, pred_input)

        loss += criterion(output, target)  # calculate the batch loss
        _, pred = torch.max(output, 1)  # convert output probabilities to predicted class
        _, y = torch.max(target, 1)

        if pred == y:
            class_c[y] += 1
        class_t[y] += 1

    return loss, class_c, class_t


def predict_dataset(model, x):
    model.eval()
    predictions = []
    for i, (pred_input, _) in enumerate(x):
        output = predict(model, pred_input)

        # convert output probabilities to predicted class
        _, pred = torch.max(output, 1)
        predictions.append(pred.item())

    return predictions


def compute_accuracy_confusion_matrix(model, loader, criterion):
    loss = 0.0

    tp, fp, fn, tn, total = 0, 0, 0, 0, 0

    model.eval()
    for pred_input, target in loader:
        output = predict(model, pred_input)

        loss += criterion(output, target)  # calculate the batch loss
        _, pred = torch.max(output, 1)  # convert output probabilities to predicted class
        _, y = torch.max(target, 1)

        total += 1
        if pred == y == 1:
            tp += 1
        elif pred == 1 and y == 0:
            fp += 1
        elif pred == 0 and y == 1:
            fn += 1
        elif pred == y == 0:
            tn += 1

    return loss, tp, fp, fn, tn, total
