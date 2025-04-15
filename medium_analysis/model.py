import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from typing import Tuple, Any

def load_and_preprocess_data(csv_path: str) -> pd.DataFrame:
    """
    Load and preprocess the dataset from CSV.
    
    Args:
        csv_path (str): Path to the CSV file containing the dataset.
        
    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    # Load dataset
    data = pd.read_csv(csv_path)

    # Handle missing values in the subtitle column
    data['subtitle'] = data['subtitle'].fillna('')

    # Preprocess data
    data['subtitle'] = data['subtitle'].apply(lambda x: x.lower())

    return data

def create_features(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Create features for the model.
    
    Args:
        data (pd.DataFrame): Preprocessed dataset.
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: Features matrix X and target variable y.
    """
    # Feature engineering
    data['title_length'] = data['title'].apply(len)
    data['subtitle_length'] = data['subtitle'].apply(len)
    data['num_images'] = data['image_count']  
    data['num_tags'] = data['tags'].apply(lambda x: len(x.split(',')) if isinstance(x, str) else 0) 

    # Vectorize text data (subtitle)
    vectorizer = TfidfVectorizer(max_features=1000)
    X_text = vectorizer.fit_transform(data['subtitle'])

    # Combine text features with other features
    X = pd.concat([
        pd.DataFrame(X_text.toarray()), 
        data[['title_length', 'subtitle_length', 'num_images', 'num_tags']]
    ], axis=1)

    # Ensure all column names are strings
    X.columns = X.columns.astype(str)

    # Target variable
    y = data['success']

    return X, y

def train_and_evaluate_model(X: pd.DataFrame, y: pd.Series) -> Tuple[RandomForestClassifier, float, str]:
    """
    Train and evaluate the Random Forest model.
    
    Args:
        X (pd.DataFrame): Features matrix.
        y (pd.Series): Target variable.
        
    Returns:
        Tuple[RandomForestClassifier, float, str]: Trained model, accuracy score, and classification report.
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return model, accuracy, report

def main() -> None:
    """Main function to run the model training and evaluation pipeline."""
    # Load and preprocess data
    data = load_and_preprocess_data('scraped_articles.csv')
    
    # Create features
    X, y = create_features(data)
    
    # Train and evaluate model
    model, accuracy, report = train_and_evaluate_model(X, y)
    
    # Print results
    print("Accuracy:", accuracy)
    print("Classification Report:\n", report)

if __name__ == "__main__":
    main()
