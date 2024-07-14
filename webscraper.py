import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import argparse

def fetch_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'lxml') 
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def extract_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    stop_phrase = ""
    try:
        print(f"Fetching URL: {url}")
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.content, 'html.parser')

            title_tag = soup.find('title')
            title = title_tag.get_text() if title_tag else 'No Title Found'

            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if not text_elements:
                print(f"No relevant tags found in {url}")
                return title, ""

            text_list = []
            for element in text_elements:
                text = element.get_text()
                if stop_phrase in text:
                    break
                text_list.append(text)

            text = "\n".join(text_list)
            print(f"Extracted text length for {url}: {len(text)}")
            return title, text
    except Exception as e:
        print(f"Failed to extract text from {url}: {e}")
        return 'No Title Found', ""

def save_to_csv(data, filename='output.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_to_json(data, filename='output.json'):
    df = pd.DataFrame(data)
    df.to_json(filename, orient='records', lines=True)
    print(f"Data saved to {filename}")

def main(sitemap_url, output_csv, output_json, delay):
    urls = fetch_urls_from_sitemap(sitemap_url)

    with open('urls.txt', 'w') as file:
        for url in urls:
            file.write(url + '\n')
    print(f"Extracted {len(urls)} URLs to urls.txt")

    data = []
    for url in urls:
        title, text = extract_text_from_url(url)
        data.append({'title': title, 'url': url, 'text': text})
        time.sleep(delay) 

    save_to_csv(data, output_csv)
    save_to_json(data, output_json)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract URLs from sitemap and fetch text from those URLs.')
    parser.add_argument('--sitemap', type=str, required=True, help='The URL of the sitemap.')
    parser.add_argument('--output-csv', type=str, default='output.csv', help='The output CSV file name.')
    parser.add_argument('--output-json', type=str, default='output.json', help='The output JSON file name.')
    parser.add_argument('--delay', type=int, default=2, help='Delay between requests to avoid rate limiting.')
    
    args = parser.parse_args()
    main(args.sitemap, args.output_csv, args.output_json, args.delay)
