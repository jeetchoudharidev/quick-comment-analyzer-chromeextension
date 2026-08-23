import pandas as pd
from datasets import load_dataset

print("Downloading dataset... (This might take a few seconds on the first run)")

# FIX: Added the "stanfordnlp/" namespace required by the newest Hugging Face update
dataset = load_dataset("stanfordnlp/imdb")

# Convert it into a Pandas DataFrame
df_train = pd.DataFrame(dataset['train'])

print("\n✅ Download Complete!")
print(f"Total reviews downloaded: {len(df_train)}")

print("\n--- Here is what Review #1 looks like ---")
print("TEXT:", df_train.iloc[0]['text'][:200], "...") 
print("LABEL (0=Bad, 1=Good):", df_train.iloc[0]['label'])