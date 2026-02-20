import csv
import os
import requests
from bs4 import BeautifulSoup

CSV_FILE = r'C:\Projects\the-index\data.csv'
URL = 'https://crmindex.net/'

def get_site_slugs():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    slugs = set()
    for link in links:
        href = link.get('href', '')
        if href.startswith('https://crmindex.net/best-crm-'):
            slug = href.replace('https://crmindex.net/', '').replace('/', '')
            slugs.add(slug)
        elif href.startswith('/best-crm-'):
            slug = href.replace('/', '')
            slugs.add(slug)
    return slugs

def get_csv_slugs():
    slugs = set()
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slugs.add(row['slug'].strip())
    return slugs

if __name__ == "__main__":
    site_slugs = get_site_slugs()
    csv_slugs = get_csv_slugs()
    
    missing_in_csv = site_slugs - csv_slugs
    missing_on_site = csv_slugs - site_slugs
    
    print(f"Total on Site: {len(site_slugs)}")
    print(f"Total in CSV: {len(csv_slugs)}")
    print(f"Missing in CSV: {len(missing_in_csv)}")
    if missing_in_csv:
        print(f"Examples: {list(missing_in_csv)[:5]}")
    print(f"Missing on Site: {len(missing_on_site)}")
