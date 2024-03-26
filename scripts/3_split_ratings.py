import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

load_dotenv()

# parse xml file:
tree = ET.parse(os.getenv("ALL_REVIEWS"))
root = tree.getroot()

# open all outfiles:
ratings_path = os.getenv("BASE_RATINGS")
outfiles = []
for i in range(1, 6):
    outfiles.append(open(f"{ratings_path}_{i}.txt", "a", encoding="utf-8"))  # add r before f?
    
# go through each review and put into respective output file:
for review in root.findall("review"):
    rating = review.find("metadata").attrib["rating"]
    review_text = review.find("text").text
    if review_text:
        # determine output file index based on rating:
        outfile_index = int(rating) - 1
        outfiles[outfile_index].write(review_text.strip() + "\n")
        
for outfile in outfiles:
    outfile.close()
    
