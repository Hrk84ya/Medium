import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from medium_analysis.model import (
    load_and_preprocess_data,
    create_features,
    train_and_evaluate_model
)

class TestModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create sample data
        self.sample_data = pd.DataFrame({
            'title': ['Test Title 1', 'Test Title 2'],
            'subtitle': ['Test Subtitle 1', 'Test Subtitle 2'],
            'image_count': [2, 3],
            'tags': ['tag1,tag2', 'tag3,tag4,tag5'],
            'success': [1, 0]
        })

    def test_load_and_preprocess_data(self):
        """Test data loading and preprocessing."""
        # Create a temporary CSV file
        test_csv = 'test_data.csv'
        self.sample_data.to_csv(test_csv, index=False)

        try:
            # Test the function
            processed_data = load_and_preprocess_data(test_csv)
            
            # Verify the preprocessing
            self.assertEqual(processed_data['subtitle'].iloc[0], 'test subtitle 1')
            self.assertEqual(processed_data['subtitle'].iloc[1], 'test subtitle 2')
            self.assertTrue(processed_data['subtitle'].notna().all())
        finally:
            # Clean up
            import os
            if os.path.exists(test_csv):
                os.remove(test_csv)

    def test_create_features(self):
        """Test feature creation."""
        # Test the function
        X, y = create_features(self.sample_data)
        
        # Verify the features
        self.assertIsInstance(X, pd.DataFrame)
        self.assertIsInstance(y, pd.Series)
        self.assertEqual(len(X), len(self.sample_data))
        self.assertEqual(len(y), len(self.sample_data))
        
        # Check if all expected features are present
        expected_features = ['title_length', 'subtitle_length', 'num_images', 'num_tags']
        for feature in expected_features:
            self.assertIn(feature, X.columns)

    @patch('medium_analysis.model.train_test_split')
    @patch('medium_analysis.model.RandomForestClassifier')
    def test_train_and_evaluate_model(self, mock_rf_class, mock_split):
        """Test model training and evaluation."""
        # Mock the train-test split
        X_train = pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        X_test = pd.DataFrame({'feature1': [5, 6], 'feature2': [7, 8]})
        y_train = pd.Series([0, 1])
        y_test = pd.Series([0, 1])
        mock_split.return_value = (X_train, X_test, y_train, y_test)

        # Mock the RandomForestClassifier
        mock_model = MagicMock()
        mock_rf_class.return_value = mock_model
        mock_model.predict.return_value = np.array([0, 1])

        # Test the function
        X = pd.DataFrame({'feature1': [1, 2, 5, 6], 'feature2': [3, 4, 7, 8]})
        y = pd.Series([0, 1, 0, 1])
        
        model, accuracy, report = train_and_evaluate_model(X, y)
        
        # Verify the results
        self.assertIsInstance(model, MagicMock)
        self.assertIsInstance(accuracy, float)
        self.assertIsInstance(report, str)
        
        # Verify that the model was trained
        mock_model.fit.assert_called_once()
        
        # Verify that predictions were made
        mock_model.predict.assert_called_once()

if __name__ == '__main__':
    unittest.main() 