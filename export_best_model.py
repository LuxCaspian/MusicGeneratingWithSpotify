import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

print("Memuat data...")
df = pd.read_csv('merged_spotify_data.csv')

def assign_mood_nlp(genre_text):
    genre = str(genre_text).lower()
    if any(k in genre for k in ['rock', 'metal', 'punk', 'dance', 'electronic', 'house', 'hip hop']):
        return 'Energetic'
    elif any(k in genre for k in ['pop', 'disco', 'country', 'reggae']):
        return 'Happy'
    elif any(k in genre for k in ['jazz', 'lo-fi', 'acoustic', 'r&b', 'chill', 'blues', 'classical']):
        return 'Chill'
    else:
        return 'Sad'

df['mood'] = df['artist_genres'].apply(assign_mood_nlp)

audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
df.dropna(subset=audio_features + ['artist_genres'], inplace=True)
df['text_feature'] = df['artist_genres']

X = df[audio_features + ['text_feature']]
y = df['mood']

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membangun Model Terbaik (Logistic Regression Hybrid)
print("Melatih Model Terbaik (Logistic Regression)...")
preprocessor = ColumnTransformer(
    transformers=[
        ('audio', StandardScaler(), audio_features),
        ('text', TfidfVectorizer(max_features=100), 'text_feature')
    ])

best_model = Pipeline([
    ('preprocessor', preprocessor), 
    ('classifier', LogisticRegression(random_state=42, max_iter=1000))
])

best_model.fit(X_train, y_train)

# Mengekspor (Save) model ke file .pkl
file_name = 'best_model_logistic_regression.pkl'
joblib.dump(best_model, file_name)

print(f"Selesai! Model terbaik telah berhasil disimpan sebagai '{file_name}'")
print("Silakan push file .pkl ini ke GitHub Anda untuk dikumpulkan sebagai jawaban Soal No. 1.")
