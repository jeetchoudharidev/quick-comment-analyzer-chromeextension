# 🌟 Quick Comment Analyzer

A Chrome Extension that analyzes the sentiment of selected text on a webpage and returns a star rating, sentiment label, and model confidence.

Select a review, comment, or paragraph, right-click it, and choose **Get Sentiment Rating**. The extension sends the selected text to the hosted Flask API and displays the result.

## ✨ Features

- **Right-click analysis:** Analyze selected text from the Chrome context menu.
- **Star rating:** Get a 1–5 star sentiment rating.
- **Sentiment category:** See a label such as Excellent, Good, Average, Bad, or Very Bad.
- **Confidence score:** View the model's positive-class probability.
- **Hosted backend:** No need to install Python or run the Flask server locally when using the deployed API.
- **Machine learning:** Uses a custom scikit-learn model trained on the IMDb movie-review dataset.

## 🚀 Use the extension (no coding required)

### 1. Download the project

1. Open the [GitHub repository](https://github.com/jeetchoudharidev/quick-comment-analyzer-chromeextension).
2. Click **Code → Download ZIP**.
3. Extract the downloaded ZIP file to a folder on your computer.

Alternatively, clone the repository:

```bash
git clone https://github.com/jeetchoudharidev/quick-comment-analyzer-chromeextension.git
```

### 2. Load it in Google Chrome

1. Open Google Chrome and visit **chrome://extensions/**.
2. Turn on **Developer mode** (top-right corner).
3. Click **Load unpacked**.
4. In the extracted/cloned project, select the **Extension** folder — not the outer project folder.
5. Confirm that the **Quick Comment Analyzer** extension appears and is enabled.

The selected folder must contain these files:

```text
Extension/
├── manifest.json
└── background.js
```

### 3. Analyze text on a webpage

1. Open a webpage that contains a review, comment, or other text.
2. Highlight the text you want to analyze.
3. Right-click the selected text.
4. Choose **Get Sentiment Rating**.
5. A popup will show the star rating, sentiment category, and AI confidence.

**Example text to try:**

> This movie was absolutely amazing! The acting was brilliant, the story was engaging, and I enjoyed every moment.

The result should indicate positive sentiment. The exact rating is determined by the trained model.

## 🌐 Hosted API

The extension is configured to use the deployed backend:

- **API service:** https://quick-comment-analyzer-chromeextension.onrender.com/
- **Health check:** https://quick-comment-analyzer-chromeextension.onrender.com/health
- **Analyze endpoint:** `POST https://quick-comment-analyzer-chromeextension.onrender.com/api/v1/analyze`

The extension sends a JSON request in this format:

```json
{
  "review": "The selected text goes here"
}
```

The API responds with the sentiment label, star rating, and confidence.

> **Note:** The backend is hosted on Render's free service. After a period of inactivity, its first request may take a little longer while the service wakes up. Keep the downloaded `Extension` folder in place; Chrome loads the unpacked extension from that local folder.

## 🧰 Developer setup (optional)

The hosted API means regular users do not need to run the backend locally. To run the Flask API for development:

1. Install Python.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Make sure `sentiment_model.pkl` is present in the project root.
4. Start the development server:

   ```bash
   python server.py
   ```

The local API will be available at `http://127.0.0.1:10000` (or the port configured by the `PORT` environment variable). Note that the extension's `background.js` is currently configured for the hosted API.

## 🛠️ Tech stack

- **Extension:** JavaScript, Chrome Extension API, Manifest V3
- **Backend:** Python, Flask, Flask-CORS, Gunicorn
- **Machine learning:** scikit-learn, TF-IDF, Logistic Regression, Joblib
- **Dataset:** IMDb movie reviews via Hugging Face Datasets (used for training)

## 🧪 Troubleshooting

- **Chrome says “Manifest file is missing or unreadable”:** In **Load unpacked**, select the `Extension` folder that directly contains `manifest.json`, not the repository's outer folder or the ZIP file.
- **The context-menu option is missing:** Make sure the extension is enabled. Open `chrome://extensions/`, click **Reload** on the extension, then refresh the webpage and select text again.
- **The request fails or takes a long time:** Check your internet connection and the [API health endpoint](https://quick-comment-analyzer-chromeextension.onrender.com/health). A free hosted service may need time to wake up after inactivity.
- **You moved or deleted the extension folder:** Chrome needs the unpacked extension files at their original location. Download/extract the project again and use **Load unpacked** to select its `Extension` folder.

## 📌 Notes

- This is a machine-learning sentiment estimate, not a guarantee of how a person feels.
- The model was trained on movie reviews, so predictions on other kinds of text may be less reliable.
- Avoid submitting private or sensitive text.
- This README describes loading the unpacked extension in Chrome. It is not currently a Chrome Web Store installation listing.
