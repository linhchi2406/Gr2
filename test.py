import requests
from bs4 import BeautifulSoup

URL = "https://soict.hust.edu.vn/can-bo/ts-nguyen-binh-minh.html"
page = requests.get(URL)

# print(page.text)
soup = BeautifulSoup(page.content, "html.parser")
# print(soup.get_text())
# results = soup.find(class="ResultsContainer")
# job_elements = soup.find("p", class_="lead")
job_elements = soup.find_all("p");
print(job_elements[1].text);

# for job_element in job_elements: 
# title_element = job_elements[0].find("h2", class_="title")
    # company_element = job_element.find("h3", class_="company")
    # location_element = job_element.find("p", class_="location")
# print(title_element.text)
    # print(company_element)
    # print(location_element)
print()

# <html><head></head><body>Sacré bleu!</body></html>