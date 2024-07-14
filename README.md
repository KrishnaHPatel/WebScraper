# Sitemap URL Extractor + Web Content Scraper

This project provides a script to extract URLs from a sitemap and fetch text content from those URLs. The extracted data is saved into CSV and JSON formats. This is useful to gathering and processing large amounts of data easily.

## Features

- Extract URLs from a sitemap.
- Fetch and extract text from web pages.
- Save extracted data to CSV and JSON files.
- Includes a Simple Command Line Interface -- which is a text-based interface where you can input commands that interact with a computer's operating system.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sitemap-url-extractor.git
   cd sitemap-url-extractor

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

## Usage

    python script.py --sitemap <SITEMAP_URL> [--output-csv <OUTPUT_CSV>] [--output-json <OUTPUT_JSON>] [--delay <DELAY>]

Arguments
1) sitemap: The URL of the sitemap.
2) output-csv: The output CSV file name (default: output.csv).
3) output-json: The output JSON file name (default: output.json).
4) delay: Delay between requests to avoid rate limiting (default: 2 seconds).
