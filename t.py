import requests
from bs4 import BeautifulSoup

URL = "https://soict.hust.edu.vn/can-bo/ths-pham-thanh-liem.html"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
name = soup.find_all("div", class_="col-inner");
test = name[1].find_all("p", class_="")
print (test.text)
# for test2 in test:
#     if(test2.find("a") != None):
#         print(test2.find("a").text)
    # if(name[0].find("p", class_="lead")):
    #     print(name[0].find("p", class_="lead").text)    
    # elif(name[0].find("p", class_="lead") == None and name[0].find_all("strong")):
        
    #     print(name[0].find("strong").text)
    #     breakpoint
    # else:
    #     breakpoint
    #     print("null")

