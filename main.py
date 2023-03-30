import requests
import re
from bs4 import BeautifulSoup
from course_catalog_scraper import scrape_courses

# Parsing for course catalog department links
root = "https://catalog.ucsd.edu"
main_page = requests.get(root + "/front/courses.html")
main_page_parser = BeautifulSoup(main_page.content, "html.parser")
a_tags = main_page_parser.find_all(href = re.compile("/courses/"))
department_links = list()
for tag in a_tags:
    path = tag["href"].replace("..", "")
    department_links.append(root + path)

scrape_courses(department_links)
