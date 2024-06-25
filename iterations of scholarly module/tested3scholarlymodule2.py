"""

This code operates off tested1scholarlymodule2.py and takes in advice from GPT on the check_name_match function. 


"""

import csv
from scholarly import scholarly, ProxyGenerator
import json
import time

class MaxTriesExceededException(Exception):
    pass

def initialize_proxy():
    pg = ProxyGenerator()
    success = pg.FreeProxies(timeout=10, wait_time=1200)
    if not success:
        raise Exception("Failed to initialize proxy.")
    scholarly.use_proxy(pg)

def search_scholar(author, year, keyword, max_retries=3, delay=10):
    retries = 0
    results = []
    while retries < max_retries:
        try:
            search_query = scholarly.search_pubs(f'{author} {year} {keyword}')
            while True:
                try:
                    pub = next(search_query)
                    print(pub)
                    results.append(pub)
                    if len(results) > 5:
                        return results
                except StopIteration:
                    return results
        except Exception as e:
            retries += 1
            print(f"Attempt {retries}/{max_retries} failed with error: {e}. Reinitializing proxy and retrying...")
            initialize_proxy()
            time.sleep(delay)
    return results

def extract_information(papers, year, author):
    extracted_data = []
    for paper in papers:
        info = {
            "title": paper.get("bib", {}).get("title"),
            "author": paper.get("bib", {}).get("author"),
            "year": paper.get("bib", {}).get("pub_year"),
            "abstract": paper.get("bib", {}).get("abstract"),
            "url": paper.get("eprint_url")
        }
        if info["year"] == year and check_name_match(info["author"], author):
            extracted_data.append(info)
            print(extracted_data)
    return extracted_data

def check_name_match(authors_list, target_name):
    # Normalize and prepare target name parts
    target_name = target_name.lower().strip()
    target_parts = target_name.split()
    if not target_parts:
        return False  # Avoid processing if target name is empty

    # Extract initials and last name from target name for pattern matching
    target_initial = target_parts[0][0]
    target_last_name = target_parts[-1]

    # Valid patterns include both full name and initials with last name
    valid_patterns = {target_name, f"{target_initial} {target_last_name}"}

    # Debugging: Show what patterns we are looking for
    print(f"Looking for patterns: {valid_patterns}")

    # Check each author against valid patterns
    for author in authors_list:
        normalized_author = author.lower().strip()
        author_parts = normalized_author.split()
        if not author_parts:
            continue

        author_initial = author_parts[0][0]
        author_full_pattern = f"{author_initial} {author_parts[-1]}"

        # Debugging: Show comparison details
        print(f"Checking author: {normalized_author} as {author_full_pattern}")

        if normalized_author in valid_patterns or author_full_pattern in valid_patterns:
            print("Match found!")
            return True

    print("No match found.")
    return False




def read_csv_and_search(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        all_extracted_data = []
        for row in csv_reader:
            author = row['author']
            year = row['year']
            keyword = row['keyword']
            print(author, year, keyword)
            papers = search_scholar(author, year, keyword)
            extracted_data = extract_information(papers, year, author)
            all_extracted_data.extend(extracted_data)
        return all_extracted_data

# Initialize proxy first
initialize_proxy()

# Read from CSV and perform search
csv_file_path = 'keywords_authors_years.csv'
extracted_data = read_csv_and_search(csv_file_path)

# Print the extracted data
for data in extracted_data:
    print(json.dumps(data, indent=2))

# Save to a JSON file
with open('scholar_data.json', 'w') as f:
    json.dump(extracted_data, f, indent=2)