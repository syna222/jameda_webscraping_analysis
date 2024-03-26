import csv
import xml.etree.ElementTree as ET
import re
from dotenv import load_dotenv
import os

load_dotenv()

# parse xml file:
tree = ET.parse(os.getenv("ALL_REVIEWS"))
root = tree.getroot()

with open(os.getenv("REVIEWS_CSV"), "a", newline="", encoding="utf-8") as csvfile:
    for review in root.findall("review"):
        rating = int(review.find("metadata").attrib["rating"])
        text = review.find("text").text  # ! not all reviews have a text!
        if text:
            # Create csv writer object:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            # modify text: remove nextlines and empty lines:
            text = re.sub("\n+", "", text)
            csvwriter.writerow([rating, text])
    
    


