import xml.etree.ElementTree as ET

# parse xml file:
tree = ET.parse("../files/all_reviews_saved.xml")
root = tree.getroot()

# open all outfiles:
outfiles = []
for i in range(1, 6):
    outfiles.append(open(f"../files/ratings_{i}.txt", "a", encoding="utf-8"))
    
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
    
