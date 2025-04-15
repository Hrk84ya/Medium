import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = pd.read_csv('scraped_articles.csv')

# Handle missing values in the subtitle column
data['subtitle'] = data['subtitle'].fillna('')

# Preprocess data
data['subtitle'] = data['subtitle'].apply(lambda x: x.lower())

# Feature engineering
data['title_length'] = data['title'].apply(len)
data['subtitle_length'] = data['subtitle'].apply(len)
data['num_images'] = data['image_count']  
data['num_tags'] = data['tags'].apply(lambda x: len(x.split(',')) if isinstance(x, str) else 0) 

# Vectorize text data (subtitle)
vectorizer = TfidfVectorizer(max_features=1000)
X_text = vectorizer.fit_transform(data['subtitle'])

# Combine text features with other features
X = pd.concat([pd.DataFrame(X_text.toarray()), data[['title_length', 'subtitle_length', 'num_images', 'num_tags']]], axis=1)

# Ensure all column names are strings
X.columns = X.columns.astype(str)

# Target variable
y = data['success']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
