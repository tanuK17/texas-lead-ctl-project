"""
This code will try filtering publications.json from folder "sm2s outputs new outputs". 

This is the first iteration of trying this. 
"""

import json

# Define the allowed authors list
allowed_authors = [
    "j elkins", "s ayoub", "k kumar", "l guyot", "m alexandrova", "m bowers", "e lang",
    "k j loescher", "j perry", "n saleh", "jules elkins", "samy ayoub", "krishna kumar",
    "layla guyot", "marina alexandrova", "matt bowers", "elon lang", "kristie j loescher",
    "jonathan perry", "navid saleh"
]

# Convert allowed_authors to lowercase for case insensitive comparison
allowed_authors = set(author.lower() for author in allowed_authors)

# Function to check if any author of a publication is allowed
def is_author_allowed(authors):
    return any(author.lower() in allowed_authors for author in authors if author)

# Path to the input file in the specified folder
input_file_path = 'publications.json'

# Read the JSON file from the specific folder
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Filter publications where at least one author is allowed
filtered_publications = [publication for publication in data if is_author_allowed(publication['bib']['author'])]

# Path to the output file
output_file_path = 'filtered_publications.json'

# Write the filtered publications to the new JSON file
with open(output_file_path, 'w') as file:
    json.dump(filtered_publications, file, indent=2)

print(f"Filtered publications have been saved to {output_file_path}.")



