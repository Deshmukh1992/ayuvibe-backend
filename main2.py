from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from sklearn.preprocessing import LabelEncoder

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained model and tokenizer
model = BertForSequenceClassification.from_pretrained('utils/my_model')
tokenizer = BertTokenizer.from_pretrained('utils/my_model')

# Load the LabelEncoder that was used during training
label_encoder = LabelEncoder()
label_encoder.classes_ = torch.load('utils/label_encoder_classes.pt')  # Assuming you've saved the encoder's classes_

# Set the model to evaluation mode
model.eval()


# Define the input data schema using Pydantic
class InputText(BaseModel):
    text: str


# Define a helper function to predict labels
def predict(text: str):

    if "hi" in text.lower() or "hello" in text.lower():
        return "Hi, I am a AyuVibe bot, Ask me about Ayurveda"

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Get the predicted label (class)
    predicted_class_id = torch.argmax(logits, dim=-1).item()
    print(predicted_class_id)

    # Map the numeric class ID to the text label
    predicted_label = label_encoder.inverse_transform([predicted_class_id])[0]
    print(predicted_label)

    return predicted_label


# Define the endpoint for prediction
@app.post("/predict/")
async def get_prediction(input_text: InputText):
    text = input_text.text
    prediction = predict(text)

    # Return the prediction result with the text label
    return {"prediction": prediction}

# If you need to run the server with Uvicorn, use this command:
# uvicorn my_fastapi_app:app --reload
