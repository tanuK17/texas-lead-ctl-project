"""
This iteration of code builds on the lsat one by incorporating proxies which help with avoiding Scholar's anti-bot measures. There's still an issue, though, that's getting thrown (see
output here): [TLDR: Max Tries received, basically indicating that the proxy's time calibration may be an issue and potentially points to using ScraperAPI as a solution instead].

Traceback (most recent call last):
  File "/Users/tanushkaushik/Downloads/Texas Lead DS/scholarlymodule1.py", line 44, in <module>
    papers = search_scholar(author, year, keyword)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/tanushkaushik/Downloads/Texas Lead DS/scholarlymodule1.py", line 10, in search_scholar
    search_query = scholarly.search_pubs(f'{author} {year} {keyword}')
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scholarly/_scholarly.py", line 160, in search_pubs
    return self.__nav.search_publications(url)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scholarly/_navigator.py", line 296, in search_publications
    return _SearchScholarIterator(self, url)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scholarly/publication_parser.py", line 53, in __init__
    self._load_url(url)
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scholarly/publication_parser.py", line 59, in _load_url
    self._soup = self._nav._get_soup(url)
                 ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scholarly/_navigator.py", line 239, in _get_soup
    html = self._get_page('https://scholar.google.com{0}'.format(url))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scholarly/_navigator.py", line 190, in _get_page
    raise MaxTriesExceededException("Cannot Fetch from Google Scholar.")
scholarly._proxy_generator.MaxTriesExceededException: Cannot Fetch from Google Scholar.

"""


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
