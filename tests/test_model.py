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
        
        # Check if all expected features are present (subtitle text + numeric)
        expected_features = ['subtitle', 'title_length', 'subtitle_length', 'num_images', 'num_tags']
        for feature in expected_features:
            self.assertIn(feature, X.columns)

    def test_train_and_evaluate_model(self):
        """Test model training and evaluation with the sklearn Pipeline."""
        # Build a dataset large enough to split
        data = pd.DataFrame({
            'title': ['Title A', 'Title B', 'Title C', 'Title D', 'Title E',
                       'Title F', 'Title G', 'Title H', 'Title I', 'Title J'],
            'subtitle': ['sub a', 'sub b', 'sub c', 'sub d', 'sub e',
                          'sub f', 'sub g', 'sub h', 'sub i', 'sub j'],
            'image_count': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
            'tags': ['t1,t2', 't3', 't1,t2,t3', 't1', 't2', 't3', 't1,t2', 't3', 't1', 't2,t3'],
            'success': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        })

        X, y = create_features(data)
        pipeline, accuracy, report = train_and_evaluate_model(X, y)

        # Pipeline should be returned, not a raw model
        from sklearn.pipeline import Pipeline
        self.assertIsInstance(pipeline, Pipeline)
        self.assertIsInstance(accuracy, float)
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)
        self.assertIsInstance(report, str)

if __name__ == '__main__':
    unittest.main() 