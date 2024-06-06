import logging
from scholarly import scholarly
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_author(author_name):
    try:
        logging.info(f"Searching for author: {author_name}")
        search_query = scholarly.search_author(author_name)
        author = next(search_query, None)
        
        if author is None:
            logging.warning(f"No author found for {author_name}")
            return None
        
        scholarly.fill(author)
        
        publications = scholarly.fill(author, sections=["publications"])
        if not publications:
            logging.info(f"No publications found for {author_name}")
            return None
        
        recent_publications = []
        for pub in author['publications']:
            if 'year' in pub['bib'] and int(pub['bib']['year']) >= 2022:
                recent_publications.append(pub['bib']['title'])
        
        return recent_publications
    except StopIteration:
        logging.error(f"Iteration stopped for {author_name}, author not found.")
        return None
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error while processing {author_name}: {e}")
        return None
    except TypeError as e:
        logging.error(f"Type error for {author_name}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error processing {author_name}: {e}")
        return None

def write_to_file(file_path, author_name, publications):
    with open(file_path, "a") as file:
        file.write(f"Recent Publications for {author_name} (2022 or later):\n")
        for pub in publications:
            file.write(f"{pub}\n")
        file.write("\n")

def main():
    # Sample data - Replace this with your actual data source
    grantees = [
        {"name": "Jules Elkins"},
        {"name": "Samy Ayoub"},
        {"name": "Krishna Kumar"},
        {"name": "Layla Guyot"},
        {"name": "Marina Alexandrova"},
        {"name": "Matt Bowers"},
        {"name": "Elon Lang"},
        {"name": "Kristie J Loescher"},
        {"name": "Jonathan Perry"},
        {"name": "Navid Saleh"}
    ]
    
    for grantee in grantees:
        author_name = grantee["name"]
        publications = process_author(author_name)
        if publications:
            logging.info(f"Recent Publications for {author_name} (2022 or later): {publications}")
            write_to_file("filtered_publications.txt", author_name, publications)
            write_to_file("output2.txt", author_name, publications)
        else:
            logging.info(f"No recent publications data available for {author_name}")

if __name__ == "__main__":
    main()
