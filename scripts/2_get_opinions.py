from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


with open("../files/gp_links.txt", "r", encoding="utf-8") as infile, open("../files/all_reviews.xml", "a",  encoding="utf-8") as outfile: 
    
    # start xml:
    outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<document>\n')
    
    for url in infile:
        opinions_superlist = []

        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()
        
        # handle cookie overlay:
        try:
            deny_cookies_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Ablehnen')]")
            deny_cookies_btn.click()
        except NoSuchElementException:
            pass
           
        # scrape reviews
        while True:
            try:
                # Get page source and parse with BeautifulSoup - better than using requests and then updating bc it allows for better dynamic interaction of page 
                page_content = driver.page_source
                soup = BeautifulSoup(page_content, "html.parser")
                
                opinion_blocks = soup.find_all("div", {"data-test-id": "opinion-block"})
                
                if opinion_blocks:
                    # for each review (block) filter date, rating and text + append this to superlist:
                    for block in opinion_blocks:
                        doctor_name = url.split("/")[3]
                        date = block.find("time", itemprop="datePublished").get("datetime")
                        rating = block.find("div", class_="rating").get("data-score")
                        comment = block.find("p", {"data-test-id": "opinion-comment"}).text.strip()
                        opinion_xml = f'<review><metadata doctor_name="{doctor_name}" date="{date}" rating="{rating}"/><text>{comment}</text></review>'
                        opinions_superlist.append(opinion_xml)
                    
                # find show more button:
                show_more_btn = driver.find_element(By.CSS_SELECTOR, "a[data-id='load-more-opinions']")
                show_more_btn.click()
                
                time.sleep(1)  # solves issue, driver wait doesn't
                
            except NoSuchElementException:  # no show more button
                break

        opinions_superlist = list(set(opinions_superlist))
        print(len(opinions_superlist))
        
        driver.quit()

        # append each doctor's opinions_superlist to global xml file:
        [outfile.write(f"{opinion}\n") for opinion in opinions_superlist]
    
    # end xml:
    outfile.write("</document>")

