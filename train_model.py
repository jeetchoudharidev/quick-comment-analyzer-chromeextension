import pandas as pd
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib

print("1. Loading dataset from disk...")
# It will load instantly this time since it's already downloaded
dataset = load_dataset("stanfordnlp/imdb")
df_train = pd.DataFrame(dataset['train'])

print("2. Building the Machine Learning Pipeline...")
# TfidfVectorizer converts text to math.
# LogisticRegression finds the patterns.
# max_features=10000 ensures the final model isn't gigabytes in size.
model = make_pipeline(
    TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000)
)

print("3. Training the AI... (Please wait 1-3 minutes. Your CPU is doing heavy math!)")
model.fit(df_train['text'], df_train['label'])

print("4. Saving the trained model to disk...")
joblib.dump(model, 'sentiment_model.pkl')
print("✅ Done! The AI brain is officially saved as 'sentiment_model.pkl'.")