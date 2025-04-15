import requests
from bs4 import BeautifulSoup
import re
import csv

# Function to scrape the Medium article
def scrape_medium_article(url):
    try:
        # Send HTTP request to fetch the content of the URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch page. Status code: {response.status_code}")
            return None

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        # Title
        title = soup.find('h1')
        title = title.text.strip() if title else None

        # Subtitle (looking for the first <h2> or any subtitle element)
        subtitle = soup.find('h2')
        subtitle = subtitle.text.strip() if subtitle else None

        # Tags: Updated to look for <div> elements with the specified class
        tags = [tag.text.strip() for tag in soup.find_all('div', class_='po ab')]

        # Title characters
        title_character = len(title) if title else 0

        # Image count
        images = soup.find_all('img')
        image_count = len(images)

        # Duration: Updated for new span with data-testid="storyReadTime"
        duration_tag = soup.find('span', {'data-testid': 'storyReadTime'})
        duration = 0
        if duration_tag:
            # Extract the numeric part of the duration (e.g., "5 min read" -> "5")
            duration_match = re.search(r'(\d+)', duration_tag.text)
            if duration_match:
                duration = int(duration_match.group(1))

        # Success flag: check if title, subtitle, and duration are present
        success = 1 if title and subtitle and duration > 0 else 0

        # Return the extracted data as a dictionary
        return {
            'title': title,
            'subtitle': subtitle,
            'tags': tags,
            'title_character': title_character,
            'image_count': image_count,
            'duration': duration,
            'success': success
        }

    except Exception as e:
        print(f"Error during scraping: {e}")
        return None


# Function to write the data to a CSV file
def write_to_csv(data, file_path):
    try:
        # Check if the file exists (if not, write headers)
        write_headers = not os.path.exists(file_path)

        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'subtitle', 'tags', 'title_character', 'image_count', 'duration', 'success']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if write_headers:
                writer.writeheader()  # Write the header only if the file is new

            writer.writerow(data)  # Write the row of data

        print(f"Data written to {file_path}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


# Read URLs from the file and scrape them
def scrape_articles_from_file(file_path, output_csv):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()

        # Strip any extra whitespace/newlines
        urls = [url.strip() for url in urls]

        # Iterate over each URL and scrape the article
        for url in urls:
            print(f"Scraping article: {url}")
            article_data = scrape_medium_article(url)
            
            if article_data:
                write_to_csv(article_data, output_csv)
            else:
                print(f"Failed to scrape article: {url}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error reading from file: {e}")


# Example usage
import os
file_path = 'medium_articles.csv'  # Path to the file containing the list of URLs
output_csv = 'scraped_articles.csv'  # Path to the output CSV file

scrape_articles_from_file(file_path, output_csv)
