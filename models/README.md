
# DEALWEAVER AI – Intent Prediction Module

## 1. Model Details

- Model: Improved BiLSTM
- Task: Negotiation Dialogue Intent Classification
- Framework: PyTorch
- Number of intent classes: 9
- Vocabulary size: 9180
- Maximum sequence length: 100

## 2. Evaluation Results

| Metric | Score |
|---|---:|
| Accuracy | 73.06% |
| Macro F1 | 70.18% |
| Weighted F1 | 73.22% |

Note: These are validation-set results, not independent test-set results.

## 3. Files Required

Keep these four files together inside the models folder:

- intent_predictor.py
- bilstm_model.pth
- vocab.json
- label_mapping.json

## 4. Dependencies

Install PyTorch:

```bash
pip install torch
```

Other preprocessing operations use Python standard libraries.

## 5. Integration in VS Code

Import the prediction function:

```python
from models.intent_predictor import predict_intent
```

Call the function:

```python
message = "buyer: I can offer $50 for this item."

intent, confidence = predict_intent(message)

print("Intent:", intent)
print("Confidence:", confidence)
```

## 6. Supported Intent Classes

1. agree
2. counter-price
3. disagree
4. inform
5. init-price
6. inquiry
7. insist
8. intro
9. vague-price

## 7. Integration Responsibility

Member 3 can use predict_intent() inside the Negotiation Analyst Agent.

The function returns:

- Predicted dialogue intent
- Prediction confidence percentage

The model only predicts dialogue intent. It does not make negotiation decisions, validate price limits, or accept deals.
