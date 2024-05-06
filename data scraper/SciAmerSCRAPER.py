import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
from datetime import datetime

def get_links(url, links_to_visit):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article", class_="article-pFLe7")

        for article in articles:
            link = article.find("a", class_="articleLink-2OMNo")["href"]
            new_url = urljoin(url, link)
            links_to_visit.add(new_url)
            if len(links_to_visit) >= 20:
                return links_to_visit

    return links_to_visit

def extract_text(links_to_visit):
    folder_name = "../Unprocessed Data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    csv_file = os.path.join(folder_name, "SciAM.csv")
    csv_exists = os.path.exists(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Website Name', 'Scraping Date', 'Scraping Time', 'Link', 'Number of Words Scraped', 'Text Scraped']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not csv_exists:
            writer.writeheader()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }

        for link in links_to_visit:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                paragraphs = soup.find_all("p")
                text = '\n'.join(paragraph.text.strip() for paragraph in paragraphs)
                num_words = len(text.split())
                scraping_date = datetime.now().strftime("%Y-%m-%d")
                scraping_time = datetime.now().strftime("%H:%M:%S")
                writer.writerow({'Website Name': 'SciAM', 'Scraping Date': scraping_date, 'Scraping Time': scraping_time, 'Link': link, 'Number of Words Scraped': num_words, 'Text Scraped': text})
            else:
                print(f"Error: Could not retrieve the page content for {link}")

def get_links_from_csv(input_csv_file):
    links_to_visit = []
    with open(input_csv_file, mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            links_to_visit.append(row['Link'])
    return links_to_visit

def get_title(link_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    response = requests.get(link_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_element = soup.find("h1", class_="article_hed-LDnzF")
        if title_element:
            if title_element.find("p"):  # Check if <h1> contains a <p> tag
                print(title_element.get_text().strip())
                return title_element.get_text().strip()
    return "Title not found"


def scrape_data(input_csv_file, output_csv_file):
    links_to_visit = get_links_from_csv(input_csv_file)
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['label', 'Scraping Date', 'Scraping Time', 'Link', 'title', 'Number of Words Scraped', 'content']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }
        for link_url in links_to_visit:
            response = requests.get(link_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                title_element = soup.find("h1", class_="elementor-heading-title elementor-size-default")  # Updated class for title
                if title_element:
                    title = title_element.get_text().strip()
                else:
                    title = "Title not found"
                paragraphs = soup.find_all("p")
                text = '\n'.join(paragraph.text.strip() for paragraph in paragraphs)
                num_words = len(text.split())
                scraping_date = datetime.now().strftime("%Y-%m-%d")
                scraping_time = datetime.now().strftime("%H:%M:%S")
                writer.writerow({'label': 'Science', 'Scraping Date': scraping_date, 'Scraping Time': scraping_time, 'Link': link_url, 'title': title, 'Number of Words Scraped': num_words, 'content': text})
            else:
                print(f"Error: Could not retrieve the page content for {link_url}")


def main():
    # url = "https://www.scientificamerican.com/technology/"
    # links_to_visit = set()
    # links_to_visit = get_links(url, links_to_visit)
    # print("Links extracted:")
    # print(links_to_visit)
    # print("\nExtracted text:")
    # extract_text(links_to_visit)
    
    input_csv_file = "../Unprocessed Data/SciAM.csv"
    output_csv_file ="../Unprocessed Data/Science.csv"
    scrape_data(input_csv_file, output_csv_file)

if __name__ == "__main__":
    main()
