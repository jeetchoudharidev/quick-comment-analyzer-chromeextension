# 🌟 Quick Comment Analyzer (Chrome Extension)

A full-stack, Machine Learning-powered Chrome Extension that analyzes the sentiment of any text on the web. Highlight a review, comment, or paragraph, right-click, and instantly see a 1-5 star rating along with the AI's confidence percentage.

## 🚀 Features
* **Custom Machine Learning Model:** Trained on 25,000 real human movie reviews using `scikit-learn`.
* **Right-Click Integration:** Seamlessly integrated into Chrome's native context menu.
* **Invisible Background Server:** The Python backend runs completely silently on your machine using `pythonw`.
* **Real-time Inference:** Fast TF-IDF vectorization and Logistic Regression for instant sentiment scoring.

## 🛠️ Tech Stack
* **Frontend:** JavaScript, HTML, Chrome Extension API (Manifest V3)
* **Backend:** Python, Flask, Flask-CORS
* **Machine Learning:** scikit-learn, Pandas, Joblib
* **Dataset Hub:** Hugging Face `datasets` library

---

## ⚙️ Installation & Setup

### Part 1: Prepare the AI Backend
1. **Clone or download this repository** to your local machine.
2. **Install the required Python dependencies:**
   ```bash
   pip install scikit-learn pandas joblib datasets flask flask-cors