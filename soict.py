import requests
import json
import csv
from bs4 import BeautifulSoup

def get_URL():
    for i in range(1,6):
        url = 'https://soict.hust.edu.vn/can-bo/page/'+ str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        get_url(soup)
        
def saveData(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print("=======================================")
    print(get_name(soup))
    get_degree(soup, get_name(soup))
    get_introduce(soup)

def get_name(soup):
    name = soup.find_all("div", class_="article-inner");
    if(name[0].find("p", class_="lead")):
        return (name[0].find("p", class_="lead").find("span").text)    
    elif(name[0].find("p", class_="lead") == None and name[0].find_all("strong")):        
        return (name[0].find("strong").text)
    else:
        return None

def get_degree(soup, name):
    if(name != None):
        degrees = soup.find_all("div", class_="col-inner")[0].find_all("p", class_="")
        for degree in degrees: 
            print(degree.text)
    else :
        print("None")

def get_introduce(soup):
    name = soup.find_all("div", class_="col-inner");
    if(len(name) > 1):
        introduce = name[1].find("p", class_="")
        if(introduce != None):
            print(introduce.text)
        else:
            print("None")

def get_url(soup):
    getUrl = soup.find_all("article");
    for link in getUrl:
        urlTeacher = link.find("a");
        saveData(urlTeacher['href']);

def write_to_json(list_input):
    try:
        with open("soict.csv", "a") as fopen:  # Open the csv file.
            csv_writer = csv.writer(fopen)
            csv_writer.writerow(list_input)
            # json.dump(list_input, fopen)
            # csv_writer.writerow(list_input)
    except:
        return False

if __name__ == '__main__':
    # get_url(soup);
    get_URL();
