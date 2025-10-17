from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import os
import sys
from transformers import BertTokenizer, TFBertForSequenceClassification
import numpy as np

app = Flask(__name__)
CORS(app)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

print("Loading model and tokenizer...")
try:
    tokenizer = BertTokenizer.from_pretrained('./', local_files_only=True)
    model = TFBertForSequenceClassification.from_pretrained('./', local_files_only=True)
    model.load_weights("tf_model.h5")
    print("Model and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise e


def predict_sentiment(text):
    try:
        inputs = tokenizer([text], return_tensors="tf", padding=True, truncation=True, max_length=128)
        outputs = model(inputs)
        pred = np.argmax(outputs.logits.numpy())
        sentiment = "positive" if pred == 1 else "negative"
        return sentiment
    except Exception as e:
        print(f"Error predicting sentiment: {str(e)}")
        return "error"


@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        sentiment = predict_sentiment(text)
        return jsonify({'sentiment': sentiment})
    except Exception as e:
        print(f"Error in analyze_sentiment endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000) 