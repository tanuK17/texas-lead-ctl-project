"""
As said in tested2scholarlymodule2.py, this is an attempt at implementing a max retries so that my code can stop taking 5 years to generate
output."""

import csv
from scholarly import scholarly, ProxyGenerator
import time

def setup_proxy_with_retries(max_retries=2):
    pg = ProxyGenerator()
    for attempt in range(max_retries):
        try:
            pg.FreeProxies()
            scholarly.use_proxy(pg)
            print("Proxy setup successful")
            return pg
        except Exception as e:
            print(f"Attempt {attempt + 1} to set up proxy failed: {e}")
            if attempt + 1 == max_retries:
                print("Max retries reached. Exiting.")
                raise
            time.sleep(1)  # Optional: wait a bit before retrying

def search_publications(author, year, keyword):
    search_query = scholarly.search_author(author)
    author_data = next(search_query, None)
    if not author_data:
        print(f"No data found for author: {author}")
        return

    author_filled = scholarly.fill(author_data)
    publications = author_filled.get('publications', [])
    
    for pub in publications:
        pub_filled = scholarly.fill(pub)
        pub_year = pub_filled.get('bib', {}).get('pub_year', None)
        pub_title = pub_filled.get('bib', {}).get('title', '')
        pub_abstract = pub_filled.get('bib', {}).get('abstract', '')

        if pub_year == str(year) and keyword.lower() in (pub_title + pub_abstract).lower():
            print(f"Author: {author}, Year: {year}, Keyword: {keyword}")
            print(f"Title: {pub_title}")
            print(f"Abstract: {pub_abstract}")
            print("-" * 80)

# Set up the proxy with retries
setup_proxy_with_retries()

# Read the CSV file
with open('keywords_authors_years.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        author = row['author']
        year = int(row['year'])
        keyword = row['keyword']
        search_publications(author, year, keyword)