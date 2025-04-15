import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from medium_analysis.medium_scraper import ArticleData, scrape_medium_article, write_to_csv, scrape_articles_from_file

class TestMediumScraper(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://medium.com/test-article"
        self.test_output_csv = "test_output.csv"
        
        # Sample article data
        self.sample_article_data = ArticleData(
            title="Test Title",
            subtitle="Test Subtitle",
            tags=["test", "python"],
            title_character=10,
            image_count=2,
            duration=5,
            success=1
        )

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_output_csv):
            os.remove(self.test_output_csv)

    @patch('requests.get')
    def test_scrape_medium_article_success(self, mock_get):
        """Test successful article scraping."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <h1>Test Title</h1>
                <h2>Test Subtitle</h2>
                <div class="po ab">test</div>
                <div class="po ab">python</div>
                <img src="test1.jpg">
                <img src="test2.jpg">
                <span data-testid="storyReadTime">5 min read</span>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        # Test the scraping function
        result = scrape_medium_article(self.test_url)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Test Title")
        self.assertEqual(result.subtitle, "Test Subtitle")
        self.assertEqual(len(result.tags), 2)
        self.assertEqual(result.image_count, 2)
        self.assertEqual(result.duration, 5)
        self.assertEqual(result.success, 1)

    @patch('requests.get')
    def test_scrape_medium_article_failure(self, mock_get):
        """Test article scraping failure."""
        # Mock the response with error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test the scraping function
        result = scrape_medium_article(self.test_url)
        
        self.assertIsNone(result)

    def test_write_to_csv(self):
        """Test writing article data to CSV."""
        # Write test data to CSV
        write_to_csv(self.sample_article_data, self.test_output_csv)
        
        # Verify the file was created and contains correct data
        self.assertTrue(os.path.exists(self.test_output_csv))
        df = pd.read_csv(self.test_output_csv)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['title'], "Test Title")
        self.assertEqual(df.iloc[0]['subtitle'], "Test Subtitle")

    @patch('medium_analysis.medium_scraper.scrape_medium_article')
    @patch('medium_analysis.medium_scraper.write_to_csv')
    def test_scrape_articles_from_file(self, mock_write, mock_scrape):
        """Test scraping articles from a file."""
        # Create a temporary file with URLs
        test_urls_file = "test_urls.txt"
        with open(test_urls_file, 'w') as f:
            f.write("https://medium.com/test1\nhttps://medium.com/test2")

        # Mock the scraping function
        mock_scrape.return_value = self.sample_article_data

        # Test the function
        scrape_articles_from_file(test_urls_file, self.test_output_csv)

        # Verify the scraping function was called twice
        self.assertEqual(mock_scrape.call_count, 2)
        # Verify the write function was called twice
        self.assertEqual(mock_write.call_count, 2)

        # Clean up
        os.remove(test_urls_file)

if __name__ == '__main__':
    unittest.main() 