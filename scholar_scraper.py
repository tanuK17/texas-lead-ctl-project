# Import necessary libraries
import requests
import pandas as pd
import time
import logging
import csv

logging.basicConfig(level=logging.INFO)

# Load the CSV file and check its structure
file_path = 'sample data - Sheet1.csv'  # Ensure the file path is correct
try:
    df = pd.read_csv(file_path)
    print(df.head())  # Display the first few rows of the dataframe
except Exception as e:
    logging.error(f"Error loading the CSV file: {e}")
    exit()

# Set up the SerpAPI key
SERPAPI_API_KEY = '4b71a74cf5c7dd1839aa9c5bddfb986ed9242e703a4ac61829cd05df5f0e7863'  # Replace with your SerpAPI key

# Define the search function
def search_google_scholar_serpapi(name, cohort_year, keywords):
    url = 'https://serpapi.com/search'
    params = {
        'engine': 'google_scholar',
        'q': name,
        'api_key': SERPAPI_API_KEY
    }
    
    response = requests.get(url, params=params)
    results = []
    if response.status_code == 200:
        data = response.json()
        logging.info(f"Received data for {name}")
        print(f"Response for {name}: {data}")  # Debug print the response
        for result in data.get('organic_results', []):
            title = result.get('title', '')
            abstract = result.get('snippet', '')
            year = result.get('publication_info', {}).get('summary', '').split(' - ')[-1]
            try:
                year = int(year)
            except ValueError:
                continue
            if year >= cohort_year:
                publication_text = f"{title} {abstract}".lower()
                weight = sum(1 for keyword in keywords if keyword.lower() in publication_text)
                if weight > 0:  # Only add if at least one keyword matches
                    results.append({
                        "title": title,
                        "author": result.get('publication_info', {}).get('authors', ''),
                        "journal": result.get('publication_info', {}).get('summary', ''),
                        "year": year,
                        "abstract": abstract,
                        "url": result.get('link', ''),
                        "weight": weight
                    })
                    logging.info(f"Added publication with weight {weight}: {title}")
    else:
        logging.error(f"Failed to retrieve data for {name} with status code {response.status_code}")
    return results

# Collect publications for each grantee
publications = []
for index, row in df.iterrows():
    grantee_name = row["Grantee Name"]
    cohort_year = row["Grantee's Cohort Year"]
    keywords = row["Grantee's Keywords"].split(", ")
    retry_count = 0
    max_retries = 5
    while retry_count < max_retries:
        try:
            results = search_google_scholar_serpapi(grantee_name, cohort_year, keywords)
            if not results:
                logging.info(f"No publications found for {grantee_name}")
            for result in results:
                publications.append({
                    "name": grantee_name,
                    "title": result['title'],
                    "author": result['author'],
                    "journal": result['journal'],
                    "year": result['year'],
                    "url": result['url'],
                    "weight": result['weight']
                })
            break
        except Exception as e:
            retry_count += 1
            logging.warning(f"Retry {retry_count}/{max_retries} for {grantee_name} due to {e}")
            time.sleep(10 * retry_count)  # Exponential backoff
            if retry_count == max_retries:
                logging.error(f"Failed to retrieve data for {grantee_name} after {max_retries} retries")
                break

# Convert to DataFrame and save to CSV
publications_df = pd.DataFrame(publications)

# Save to CSV with verification
csv_file_path = 'publications_filtered.csv'
try:
    publications_df.to_csv(csv_file_path, index=False)
    # Verify the CSV writing process
    verification_df = pd.read_csv(csv_file_path)
    if not verification_df.empty:
        logging.info("Data successfully written to publications_filtered.csv")
    else:
        logging.warning("CSV file is empty after writing data.")
except Exception as e:
    logging.error(f"Error writing or reading the CSV file: {e}")

# Display the resulting DataFrame
try:
    print(verification_df.head())
except NameError:
    logging.error("Verification DataFrame is not defined.")
