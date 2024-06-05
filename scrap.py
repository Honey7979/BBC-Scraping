import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import csv
import os

# List of user agents to simulate different browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
]

# Function to scrape headlines from a specific category on BBC News
def scrape_bbc_headlines(category):
    base_url = 'https://www.bbc.com'
    category_url = f"{base_url}/{category}"
    retries = 5

    for i in range(retries):
        try:
            user_agent = random.choice(USER_AGENTS)
            headers = {'User-Agent': user_agent}
            response = requests.get(category_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all elements that are likely to contain headlines and store them in a set for uniqueness
            headlines = set()
            for tag in soup.find_all(['h3', 'h2']):
                if tag and tag.get_text(strip=True):
                    headlines.add(tag.get_text(strip=True))

            return headlines
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                print("Max retries reached. Exiting.")
                return set()  # Return empty set on failure

# Function to save headlines to CSV file
def save_to_csv(headlines, category):
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"files/{category}_{current_date}.csv"

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write headlines to CSV
        for headline in headlines:
            writer.writerow([headline])

    print(f"Headlines saved to {filename}")

# Main function to execute the scraping and save headlines to CSV
if __name__ == "__main__":
    categories = ['technology', 'business', 'sport', 'culture', 'travel', 'innovation']  # Add more categories as needed

    for category in categories:
        headlines = scrape_bbc_headlines(category)
        if headlines:
            save_to_csv(headlines, category)
        else:
            print(f"No headlines found for {category}")
