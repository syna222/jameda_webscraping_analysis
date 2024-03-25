from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

# get names of all general practicioners (private and state insurance) in Cologne
doctor_pages = []
doctor_namelinks = []

base_url = r"https://www.jameda.de/suchen?q=Allgemeinmediziner%20(Hausarzt)&loc=K%C3%B6ln&filters[entity_type][]=doctor&filters[specializations][]=33&sorter=rating" #&page=" #until no more pages

# get max page number:
page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")
ul_element= soup.find("ul", class_="pagination pagination-lg")
last_li = ul_element.find_all("a", class_="page-link")[-2]
max_page_num = int(last_li.text.strip())

for i in range(1, max_page_num + 1):
    url = base_url + "&page=" + str(i)
    doctor_pages.append(url)

with open("../files/gp_links.txt", "a") as file:
    # for each page in doctor_pages, visit page, grab all doctor names/links and append them to the doctor_namelinks list:
    for page_link in doctor_pages:
        page = requests.get(page_link)
        soup = BeautifulSoup(page.content, "html.parser")
        doctor_links = soup.find_all("a", class_="text-body")
        [file.write(f"{link.get('href')}\n") for link in doctor_links]

[print(dnl) for dnl in doctor_namelinks]   #all GPs in Cologne



