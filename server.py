import os
import logging
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)
CORS(app)

# Load the trained model from the same directory as this file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "sentiment_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    logging.info("Custom ML model loaded successfully.")

    # Identify the positive class instead of assuming predict_proba index 1.
    classes = getattr(model, "classes_", None)
    if classes is None or len(classes) != 2:
        raise ValueError("Expected a binary classifier with exactly two classes.")

    positive_candidates = [i for i, label in enumerate(classes) if str(label).lower() in ("1", "positive", "pos")]
    if positive_candidates:
        POSITIVE_CLASS_INDEX = positive_candidates[0]
    else:
        # The training script uses the IMDB dataset labels (0 = negative, 1 = positive).
        POSITIVE_CLASS_INDEX = 1

except Exception:
    logging.exception("Could not load or validate sentiment_model.pkl")
    raise


def get_rating_from_probability(pos_prob: float):
    """Convert the predicted positive-class probability into a 1–5 star rating."""
    if pos_prob >= 0.80:
        return "Excellent 😊", 5
    elif pos_prob >= 0.60:
        return "Good 🙂", 4
    elif pos_prob >= 0.40:
        return "Average 😐", 3
    elif pos_prob >= 0.20:
        return "Bad 😞", 2
    return "Very Bad 😡", 1


@app.get("/")
def index():
    return jsonify({
        "service": "Quick Comment Analyzer API",
        "status": "online"
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None}), 200


@app.post("/api/v1/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    review_text = str(data.get("review") or "").strip()

    if not review_text:
        return jsonify({"error": "Empty review."}), 400

    if len(review_text) > 10000:
        return jsonify({"error": "Review is too long. Maximum length is 10000 characters."}), 413

    try:
        probabilities = model.predict_proba([review_text])[0]
        positive_probability = float(probabilities[POSITIVE_CLASS_INDEX])

        label, stars = get_rating_from_probability(positive_probability)

        return jsonify({
            "label": label,
            "stars": "⭐" * stars,
            "confidence": f"{positive_probability * 100:.1f}%"
        }), 200

    except Exception:
        logging.exception("Sentiment prediction failed")
        return jsonify({"error": "Sentiment analysis failed."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
