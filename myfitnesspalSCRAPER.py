import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
from datetime import datetime

def get_links(url, links_to_visit):
    # Define a User-Agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

    # Send a GET request to the URL with the headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the specific <div> containing the links
        div = soup.find("div", class_="elementor-loop-container elementor-grid")
        if div:
            # Find all <a> tags within the specific <div>
            for link in div.find_all("a", href=True):
                new_url = urljoin(url, link["href"])
                if new_url not in links_to_visit:
                    links_to_visit.add(new_url)
                    if len(links_to_visit) >= 20:
                        return links_to_visit
                    # Recursively call get_links to get links from this page as well
                    get_links(new_url, links_to_visit)

    return links_to_visit

def extract_text(links_to_visit):
    # Create a folder if it doesn't exist
    folder_name = "Unprocessed Data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create a CSV file
    csv_file = os.path.join(folder_name, "MyFitnessPal.csv")
    csv_exists = os.path.exists(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Website Name', 'Scraping Date', 'Scraping Time', 'Link', 'Number of Words Scraped', 'Text Scraped']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not csv_exists:
            writer.writeheader()
        # Define a User-Agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }

        # Loop over each link in the set
        for link in links_to_visit:
            # Send a GET request to the URL with the headers
            response = requests.get(link, headers=headers)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")
                # Find all <p> tags
                paragraphs = soup.find_all("p")
                # Extract the text content from each paragraph
                text = '\n'.join(paragraph.text.strip() for paragraph in paragraphs)
                # Count number of words scraped
                num_words = len(text.split())
                # Get scraping date and time
                scraping_date = datetime.now().strftime("%Y-%m-%d")
                scraping_time = datetime.now().strftime("%H:%M:%S")
                # Write the data to the CSV file
                writer.writerow({'Website Name': 'MyFitnessPal', 'Scraping Date': scraping_date, 'Scraping Time': scraping_time, 'Link': link, 'Number of Words Scraped': num_words, 'Text Scraped': text})
            else:
                print(f"Error: Could not retrieve the page content for {link}")

def main():
    # url = "https://blog.myfitnesspal.com/best-foods-semaglutide-according-to-expert/"'
    url = "https://blog.myfitnesspal.com/category/nutrition-basics/food-facts/"
    links_to_visit = set()
    links_to_visit = get_links(url, links_to_visit)
    print("Links extracted:")
    print(links_to_visit)
    print("\nExtracted text:")
    extract_text(links_to_visit)

if __name__ == "__main__":
    main()
