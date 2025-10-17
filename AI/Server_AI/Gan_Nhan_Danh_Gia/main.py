import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import numpy as np

tokenizer = BertTokenizer.from_pretrained('./', local_files_only=True)
model = TFBertForSequenceClassification.from_pretrained('./', local_files_only=True)
model.load_weights("tf_model.h5")

def predict_sentiment(text):
    inputs = tokenizer([text], return_tensors="tf", padding=True, truncation=True, max_length=128)
    outputs = model(inputs)
    pred = np.argmax(outputs.logits.numpy())
    sentiment = "positive" if pred == 1 else "negative"
    return sentiment

while True:
    review = input("Nhập đánh giá (gõ 'x' để thoát): ")
    if review.strip().lower() == 'x':
        break
    if review.strip():
        sentiment = predict_sentiment(review.strip())
        print(f"→ Kết quả: {sentiment}\n")