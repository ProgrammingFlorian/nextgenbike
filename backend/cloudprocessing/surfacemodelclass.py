import torch
import torch.nn as nn


class SurfaceModel(nn.Module):
    def __init__(self, input_size=1, output_size=4, hidden_dim=2, n_layers=1): # TODO: Parameter default values
        super(SurfaceModel, self).__init__()

        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        # Todo: Define
        # defining Layers
        # RNN layer
        self.rnn = nn.RNN(input_size, hidden_dim, n_layers, batch_first=True)
        # fully connected Layer
        self.fc = nn.Linear(hidden_dim, output_size)

    def forward(self, x):
        # Todo: Apply
        batch_size = x.size(0)

        # Initializing hidden state for first input using method defined below
        hidden = self.init_hidden(batch_size)

        # Passing in the input and hidden state into the model and obtaining outputs
        out, hidden = self.rnn(x, hidden)

        # Reshaping the outputs such that it can be fit into the fully connected layer
        out = out.contiguous().view(-1, self.hidden_dim)
        out = self.fc(out)

        return out, hidden

    def init_hidden(self, batch_size):
        # This method generates the first hidden state of zeros which we'll use in the forward pass
        # We'll send the tensor holding the hidden state to the device we specified earlier as well
        hidden = torch.zeros(self.n_layers, batch_size, self.hidden_dim)
        return hidden
