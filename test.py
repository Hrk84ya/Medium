import requests
from bs4 import BeautifulSoup

def extract_article_data(url):
    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load the page")

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title (assuming title is inside <h1>)
    title = soup.find('h1').text if soup.find('h1') else 'No title found'
    
    # Extract subtitle (you may need to adjust this selector based on the webpage's structure)
    subtitle = soup.find('h2').text if soup.find('h2') else 'No subtitle found'
    
    # Extract tags (adjust based on your website's tag structure)
    tags = ', '.join([tag.text for tag in soup.find_all('a', {'class': 'tag'})])  # Adjust based on the website structure

    return {
        'title': title,
        'subtitle': subtitle,
        'tags': tags
    }

# Example usage:
url = 'https://medium.com/@hrk84ya/natural-language-processing-nlp-for-beginners-unlocking-the-power-of-text-210b5b58e48a'
article_data = extract_article_data(url)
print(article_data)
