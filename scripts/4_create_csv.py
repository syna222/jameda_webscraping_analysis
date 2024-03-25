import csv
import xml.etree.ElementTree as ET
import re

# parse xml file:
tree = ET.parse("../files/all_reviews_saved.xml")
root = tree.getroot()

with open("reviews.csv", "a", newline="", encoding="utf-8") as csvfile:
    for review in root.findall("review"):
        rating = int(review.find("metadata").attrib["rating"])
        text = review.find("text").text  # ! not all reviews have a text!
        if text:
            # Create csv writer object:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            # modify text: remove nextlines and empty lines:
            text = re.sub("\n+", "", text)
            csvwriter.writerow([rating, text])
    
    


