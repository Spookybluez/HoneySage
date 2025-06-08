import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle
import os

DATA_PATH = "../sample_attack_training_data.csv"
MODEL_PATH = "../model/classifier.pkl"

# Load and preprocess the dataset
df = pd.read_csv(DATA_PATH)
df['combined'] = df['username'].fillna('') + ' ' + df['password'].fillna('')

# Vectorize the combined text
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['combined'])
y = df['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump((vectorizer, clf), f)

print(f"Model saved to {MODEL_PATH}")
