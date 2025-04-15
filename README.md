# Medium Article Analysis Project

This project analyzes Medium articles using web scraping and machine learning techniques to understand what makes articles successful.

## Features

- Web scraping of Medium articles
- Data preprocessing and feature engineering
- Machine learning model for article success prediction
- Comprehensive test suite
- Type hints and documentation

## Project Structure

```
.
├── medium_analysis/           # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── medium_scraper.py     # Web scraping module
│   └── model.py              # Machine learning model
├── tests/                    # Test directory
│   ├── __init__.py           # Test package initialization
│   ├── conftest.py           # Test configuration
│   ├── test_scraper.py       # Tests for scraper
│   └── test_model.py         # Tests for model
├── setup.py                  # Package setup file
├── pytest.ini                # Pytest configuration
├── scraped_articles.csv      # Scraped article data
└── medium_articles.csv       # List of article URLs
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd medium-analysis
```

2. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

## Usage

### 1. Scraping Articles

To scrape articles from Medium:

```python
from medium_analysis.medium_scraper import scrape_articles_from_file

# Scrape articles from a file containing URLs
scrape_articles_from_file('medium_articles.csv', 'scraped_articles.csv')
```

### 2. Training the Model

To train the machine learning model:

```python
from medium_analysis.model import main

# Train and evaluate the model
main()
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=medium_analysis

# Run tests in parallel
pytest -n auto
```

## Data Format

### Input Data (medium_articles.csv)
- One URL per line
- URLs should point to Medium articles

### Scraped Data (scraped_articles.csv)
- title: Article title
- subtitle: Article subtitle
- tags: Comma-separated list of tags
- title_character: Number of characters in title
- image_count: Number of images in article
- duration: Estimated reading time in minutes
- success: Binary indicator of article success

## Model Features

The model uses the following features:
- Title length
- Subtitle length
- Number of images
- Number of tags
- TF-IDF features from subtitle text

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Beautiful Soup for web scraping
- scikit-learn for machine learning
- Medium for the article platform 