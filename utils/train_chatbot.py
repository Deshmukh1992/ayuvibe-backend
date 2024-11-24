from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset


# Define the tokenize function to handle both input and label tokenization
def tokenize_function(examples, tokenizer, max_length=128):
    # Tokenize the text (input)
    inputs = tokenizer(examples['text'], truncation=True, padding="max_length", max_length=max_length)
    # Use the same input for labels if 'label' is not explicitly provided
    labels = tokenizer(examples.get('label', examples['text']), truncation=True, padding="max_length",
                       max_length=max_length)
    inputs['labels'] = labels['input_ids']
    return inputs


if __name__ == "__main__":
    # Load model and tokenizer
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token  # Ensure padding token is set

    # Load dataset
    dataset = load_dataset('json', data_files={
        'train': r'D:\All_Projects\ayuvibe\ayuvibe-backend\dataset\ayurvedic_conversations.json'})

    # Tokenize dataset
    tokenized_datasets = dataset.map(lambda examples: tokenize_function(examples, tokenizer, max_length=128),
                                     batched=True)

    # Set training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        save_steps=10_000,
        save_total_limit=2,
        fp16=True  # Mixed precision training for faster performance on GPUs
    )

    # Train the model
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
    )

    trainer.train()
