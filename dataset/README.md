
# Dataset Documentation

## Dataset
Stanford NLP Craigslist Bargains.

## Processed files
- processed/train_messages.csv
- processed/validation_messages.csv

## Extracted message counts
- Training: 26,316 messages
- Validation: 2,996 messages
- Test: 0 usable labelled messages

## Fields
The processed data includes conversation ID, message index,
buyer/seller role, utterance, role-prefixed text, intent,
price and split.

## Intent classes
agree, counter-price, disagree, inform, init-price,
inquiry, insist, intro and vague-price.

## Evaluation limitation
The original test split had no usable intent labels.
The reported model metrics are validation results,
not independent test-set results.
