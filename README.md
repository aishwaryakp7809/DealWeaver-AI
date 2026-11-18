
# DEALWEAVER AI
## AI-Based Multi-Agent Buyer-Seller Negotiation System

### Project Overview
DEALWEAVER AI simulates buyer-seller negotiations using four agents:
1. Buyer Agent
2. Seller Agent
3. Mediator Agent
4. Negotiation Analyst Agent

### Member 1: Dataset, ML and Deep Learning

Dataset: Stanford NLP Craigslist Bargains

- Training messages: 26,316
- Validation messages: 2,996
- Intent classes: 9

### Models Developed

1. Logistic Regression with TF-IDF
2. Baseline BiLSTM using PyTorch
3. Improved BiLSTM using PyTorch

### Model Comparison

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Logistic Regression | 71.16% | 65.75% | 71.50% |
| Baseline BiLSTM | 67.32% | 66.68% | 67.17% |
| Improved BiLSTM | 73.06% | 70.18% | 73.22% |

Selected model: Improved BiLSTM.

### Project Structure

- dataset/: Dataset documentation and processed data
- models/: Trained ML and DL models
- evaluation/: Metrics, reports and visualizations
- agents/: Negotiation agent implementations (integration stage)
- app/: Streamlit application (integration stage)

### Model Deliverables

- intent_model.joblib
- vectorizer.joblib
- bilstm_model.pth
- vocab.json
- label_mapping.json
- label_encoder.pkl

### Evaluation Deliverables

- evaluation_metrics.json
- classification_report.json
- confusion_matrix.csv
- model_comparison.csv
- training_history.json
- plots/

### Technology Stack

Python, Pandas, NumPy, Scikit-learn, PyTorch,
Matplotlib, Seaborn and Google Colab.

### Evaluation Note

The original test split contained no usable labelled
intent messages. Therefore, all reported performance
metrics are validation results, not independent test results.

The intent classifier predicts dialogue intent.
Price-limit validation and negotiation decisions are
handled separately by rule-based agent logic.

### Future Integration

The trained classifier will be integrated into the
Negotiation Analyst Agent and connected to the
Buyer, Seller and Mediator Agents.
