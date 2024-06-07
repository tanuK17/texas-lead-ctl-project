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
            if len(results) > 2:
                break
        except StopIteration:
            break
    return results

def extract_information(papers, year, author):
    extracted_data = []
    for paper in papers:
        if paper.get("bib").get("pub_year")>=year and author.split(" ").intersection(paper.get("bib").get("author")[0].split(" ")):
            info = {
                "title": paper.get("bib").get("title"),
                "author": paper.get("bib").get("author"),
                "year": paper.get("bib").get("pub_year"),
                "abstract": paper.get("bib").get("abstract"),
                "url": paper.get("eprint_url")
            }
            extracted_data.append(info)

    print(extracted_data)
    return extracted_data

# Example search
author = "samy ayoub"
year = "2023"
keyword = "advocate, aim, educate, research"
papers = search_scholar(author, year, keyword)
extracted_data = extract_information(papers, year, author)

# # Print the extracted data
# for data in extracted_data:
#     print(json.dumps(data, indent=2))

# # Save to a JSON file
# with open('scholar_data.json', 'w') as f:
#     json.dump(extracted_data, f, indent=2)

samy in paper.get("bib").get("author")
ayoub in paper.get("bib").get("author")