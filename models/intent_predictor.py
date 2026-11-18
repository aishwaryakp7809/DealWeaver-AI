
import os
import re
import json
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence


# Recreate the exact Improved BiLSTM architecture
class NegotiationBiLSTM(nn.Module):

    def __init__(self, vocab_size, embedding_dim, hidden_dim,
                 num_classes, dropout):

        super(NegotiationBiLSTM, self).__init__()

        self.embedding = nn.Embedding(
            vocab_size, embedding_dim, padding_idx=0
        )

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            batch_first=True,
            bidirectional=True
        )

        self.dropout = nn.Dropout(dropout)

        self.fc1 = nn.Linear(hidden_dim * 2, 128)
        self.relu = nn.ReLU()

        self.fc2 = nn.Linear(128, 64)
        self.output = nn.Linear(64, num_classes)

    def forward(self, x, lengths):

        embedded = self.embedding(x)

        packed = pack_padded_sequence(
            embedded,
            lengths.cpu(),
            batch_first=True,
            enforce_sorted=False
        )

        _, (hidden, _) = self.lstm(packed)

        forward_hidden = hidden[-2]
        backward_hidden = hidden[-1]

        combined = torch.cat(
            (forward_hidden, backward_hidden), dim=1
        )

        combined = self.dropout(combined)

        x = self.fc1(combined)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = self.relu(x)

        return self.output(x)


# Locate saved model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "bilstm_model.pth")
VOCAB_PATH = os.path.join(BASE_DIR, "vocab.json")
LABEL_PATH = os.path.join(BASE_DIR, "label_mapping.json")


# Select CPU or GPU
DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# Load saved checkpoint
checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=False
)

# Load vocabulary
with open(VOCAB_PATH, "r") as f:
    VOCAB = json.load(f)

# Load label mapping
with open(LABEL_PATH, "r") as f:
    LABEL_MAPPING = json.load(f)

# Reverse mapping: class ID -> intent
ID_TO_LABEL = {
    index: label
    for label, index in LABEL_MAPPING.items()
}


# Initialize model using saved configuration
model = NegotiationBiLSTM(
    vocab_size=checkpoint["vocab_size"],
    embedding_dim=checkpoint["embedding_dim"],
    hidden_dim=checkpoint["hidden_dim"],
    num_classes=checkpoint["num_classes"],
    dropout=checkpoint["dropout"]
).to(DEVICE)

# Load trained weights
model.load_state_dict(checkpoint["model_state_dict"])

model.eval()

MAX_LEN = checkpoint["max_len"]


# Public prediction function
def predict_intent(message):

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Message must be a non-empty string.")

    # Tokenization must match training preprocessing
    tokens = re.findall(
        r"\b\w+\b|[^\w\s]",
        message.lower()
    )

    # Convert words into token IDs
    token_ids = [
        VOCAB.get(token, 1)
        for token in tokens
    ]

    # Truncate to maximum sequence length
    token_ids = token_ids[:MAX_LEN]

    sequence_length = len(token_ids)

    # Padding
    token_ids += [0] * (MAX_LEN - sequence_length)

    input_tensor = torch.tensor(
        [token_ids],
        dtype=torch.long
    ).to(DEVICE)

    length_tensor = torch.tensor(
        [sequence_length],
        dtype=torch.long
    )

    # Prediction
    with torch.no_grad():

        outputs = model(input_tensor, length_tensor)

        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted_index = torch.max(
            probabilities, dim=1
        )

    predicted_intent = ID_TO_LABEL[
        predicted_index.item()
    ]

    confidence_score = round(
        confidence.item() * 100, 2
    )

    return predicted_intent, confidence_score


print("DEALWEAVER Intent Predictor loaded successfully!")
print("Device:", DEVICE)
print("Model: Improved BiLSTM")
print("Number of intent classes:", len(LABEL_MAPPING))
