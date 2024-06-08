from scholarly import scholarly, ProxyGenerator
import json

# Setup Proxy (optional, but recommended)
pg = ProxyGenerator()
pg.FreeProxies()  # This will use free proxies
scholarly.use_proxy(pg)

def search_scholar(author, year, keyword):
    search_query = scholarly.search_pubs(f'{author} {year} {keyword}')
    # print(search_query)
    results = []
    while True:
        try:
            pub = next(search_query)
            # print(pub)
            results.append(pub)
            if len(results) > 5:
                break
        except StopIteration:
            break
    return results

def extract_information(papers, year, author):
    extracted_data = []
    for paper in papers:
        info = {
            "title": paper.get("bib").get("title"),
            "author": paper.get("bib").get("author"),
            "year": paper.get("bib").get("pub_year"),
            "abstract": paper.get("bib").get("abstract"),
            "url": paper.get("eprint_url")
        }
        # print(info)
        # print(check_name_match(info["author"], author), info["year"]==year)
        
        if info["year"]==year and check_name_match(info["author"], author):
            extracted_data.append(info)

    # print(extracted_data)
    return extracted_data

# Function to check if the name matches any element in the array
def check_name_match(array, name):
    # Normalize the name
    name_normalized = name.lower()
    # Split the name into words
    name_words = set(name_normalized.split())
    # print(name_words)

    # Iterate through the array and check for matches
    for element in array:
        # Normalize the element
        element_normalized = element.lower()
        # Split the element into words
        element_words = set(element_normalized.split())
        # print(element_words)
        
        # Check if all words in element match with any words in the name
        if element_words.intersection(name_words):
            return True
    return False

# Example search
author = "samy ayoub"
year = "2023"
keyword = "advocate, aim, educate, research"
papers = search_scholar(author, year, keyword)
extracted_data = extract_information(papers, year, author)
print(extracted_data)