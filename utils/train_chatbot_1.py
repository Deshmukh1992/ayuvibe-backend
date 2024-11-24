import json
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
from sklearn.preprocessing import LabelEncoder

# Load the dataset
with open(r"D:\All_Projects\ayuvibe\ayuvibe-backend\dataset\ayurvedic_conversations.json", "r") as f:
    data = json.load(f)

# Convert the dataset into a DataFrame
df = pd.DataFrame(data)
print(df.head())

# Label Encoding - Convert textual labels into integers
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])
print(df.head())  # Check the updated DataFrame with encoded labels

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(df['label'].unique()))


# Tokenize the data
def tokenize_function(examples):
    # Tokenize the text data and return input_ids and attention_mask
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=128)


# Convert the DataFrame to a Hugging Face Dataset
dataset = Dataset.from_pandas(df)

# Tokenize the data
tokenized_datasets = dataset.map(tokenize_function, batched=True)


# Convert tokenized data into PyTorch tensors
def format_example(example):
    return {
        'input_ids': torch.tensor(example['input_ids'], dtype=torch.long),
        'attention_mask': torch.tensor(example['attention_mask'], dtype=torch.long),
        'label': torch.tensor(example['label'], dtype=torch.long)  # Ensure label is also a tensor
    }


# Apply formatting to the tokenized dataset
tokenized_datasets = tokenized_datasets.map(format_example)

# Split the dataset into training and testing
train_test_split1 = tokenized_datasets.train_test_split(test_size=0.2)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Set up Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_test_split1['train'],
    eval_dataset=train_test_split1['test']
)

# Fine-tune the model
trainer.train()

# Evaluate the model
trainer.evaluate()

model.save_pretrained('./my_model')
tokenizer.save_pretrained('./my_model')

# Save the LabelEncoder classes after training
torch.save(label_encoder.classes_, './label_encoder_classes.pt')
