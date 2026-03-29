import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
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
        Tuple[pd.DataFrame, pd.Series]: Features DataFrame (includes 'subtitle' text
            column and numeric feature columns) and target variable y.
    """
    # Feature engineering
    data = data.copy()
    data['title_length'] = data['title'].apply(len)
    data['subtitle_length'] = data['subtitle'].apply(len)
    data['num_images'] = data['image_count']  
    data['num_tags'] = data['tags'].apply(lambda x: len(x.split(',')) if isinstance(x, str) else 0) 

    # Return subtitle text alongside numeric features; TF-IDF is applied later in the pipeline
    X = data[['subtitle', 'title_length', 'subtitle_length', 'num_images', 'num_tags']]
    y = data['success']

    return X, y

def train_and_evaluate_model(X: pd.DataFrame, y: pd.Series) -> Tuple[Pipeline, float, str]:
    """
    Train and evaluate the model using an sklearn Pipeline so that
    TF-IDF vectorization is fit only on training data.
    
    Args:
        X (pd.DataFrame): Features DataFrame with a 'subtitle' text column
            and numeric columns.
        y (pd.Series): Target variable.
        
    Returns:
        Tuple[Pipeline, float, str]: Trained pipeline, accuracy score, and classification report.
    """
    # Split data *before* any text vectorization
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    numeric_features = ['title_length', 'subtitle_length', 'num_images', 'num_tags']

    preprocessor = ColumnTransformer(
        transformers=[
            ('tfidf', TfidfVectorizer(max_features=1000), 'subtitle'),
            ('num', 'passthrough', numeric_features),
        ]
    )

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42)),
    ])

    # Fit only on training data
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return pipeline, accuracy, report

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
