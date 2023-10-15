import torch
import numpy as np


def compute_accuracy(model, loader, device, criterion):
    loss = 0.0
    class_c = list(0. for _ in range(10))
    class_t = list(0. for _ in range(10))

    model.eval()
    for i, (x, y) in enumerate(loader):
        (x, y) = (x.to(device), y.to(torch.float32).to(device))  # send the input to the device
        output = model(x)

        temp_loss = criterion(output, y)  # calculate the batch loss
        temp_loss += temp_loss.item() * x.size(0)  # update training loss
        # convert output probabilities to predicted class
        _, pred = torch.max(output, 1)
        _, y = torch.max(y, 1)
        # compare predictions to true label
        correct_tensor = pred.eq(y)
        correct = np.squeeze(correct_tensor)

        for j in range(len(y.data)):  # calculate training accuracy for each object class
            label = y.data[j]
            class_c[label] += correct[j].item()
            class_c[label] += 1

    return loss, class_c, class_t
