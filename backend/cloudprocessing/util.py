import torch

import backend.config as config


def compute_accuracy(model, loader, criterion, n_cols):
    loss = 0.0
    class_c = list(0. for _ in range(len(config.classes)))
    class_t = list(0. for _ in range(len(config.classes)))

    model.eval()
    for i, (training_input, target) in enumerate(loader):
        hidden = model.initHidden()

        for data_row in training_input:
            for i in range(0, len(data_row), n_cols):
                model_input = data_row[None, i:i + n_cols].float()
                output, hidden = model(model_input, hidden)

        temp_loss = criterion(output, target)  # calculate the batch loss
        temp_loss += temp_loss.item() * training_input.size(0)  # update training loss
        # convert output probabilities to predicted class
        _, pred = torch.max(output, 1)
        _, y = torch.max(target, 1)

        if pred == y:
            class_c[y] += 1
        class_t[y] += 1

    return loss, class_c, class_t
