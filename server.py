import os
import sys
import logging
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

# Prevent windowless execution crashes
if sys.stdout is None: sys.stdout = open(os.devnull, "w")
if sys.stderr is None: sys.stderr = open(os.devnull, "w")

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = Flask(__name__)
CORS(app)

# 1. Load your newly trained AI model!
try:
    model = joblib.load('sentiment_model.pkl')
    logging.info("Custom ML Model loaded successfully.")
except Exception as e:
    logging.error(f"Could not load model: {e}")
    sys.exit(1)

def get_rating_from_probability(pos_prob: float):
    """Converts the AI's confidence percentage into a 1-5 star scale."""
    if pos_prob >= 0.80: return "Excellent 😊", 5
    elif pos_prob >= 0.60: return "Good 🙂", 4
    elif pos_prob >= 0.40: return "Average 😐", 3
    elif pos_prob >= 0.20: return "Bad 😞", 2
    else: return "Very Bad 😡", 1

@app.route("/api/v1/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    review_text = str(data.get("review", "")).strip()
    
    if not review_text:
        return jsonify({"error": "Empty review."}), 400

    try:
        # predict_proba returns [[Negative_Prob, Positive_Prob]]
        # We want the Positive probability (index 1)
        probabilities = model.predict_proba([review_text])[0]
        positive_probability = probabilities[1]
        
        label, stars = get_rating_from_probability(positive_probability)
        
        return jsonify({
            "label": label,
            "stars": "⭐" * stars,
            "confidence": f"{positive_probability * 100:.1f}%" # New feature!
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)