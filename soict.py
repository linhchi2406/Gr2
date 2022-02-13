import requests
import json
import csv
from bs4 import BeautifulSoup
import pymysql

mydb = pymysql.connect(
  host="localhost",
  port =3308,
  user="root",
  password="linhchi",
  db="soict"
)
def get_URL(mydb):
    for i in range(1,6):
        url = 'https://soict.hust.edu.vn/can-bo/page/'+ str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        get_url(soup, mydb)
        
def saveData(url, mydb):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print("=======================================")
    cur = mydb.cursor()
    sql = "INSERT INTO soict1 (fullname, degree, url, introduce, research) VALUES (%s, %s, %s, %s, %s)"
    val = (get_name(soup), get_degree(soup, get_name(soup)), url, get_introduce(soup),get_research(soup, get_name(soup)) )
    cur.execute(sql, val)
    mydb.commit()

# Tên của giảng viên
def get_name(soup):
    name = soup.find_all("div", class_="article-inner");
    if(name[0].find("p", class_="lead")):
        return (name[0].find("p", class_="lead").find("span").text)    
    elif(name[0].find("p", class_="lead") == None and name[0].find_all("strong")):        
        return (name[0].find("strong").text)
    else:
        return None
#Chức vị trong trường, bộ môn giảng dạy của giảng viên
def get_degree(soup, name):
    if(name != None):
        degrees = soup.find_all("div", class_="col-inner")[0].find_all("p", class_="")
        for degree in degrees: 
            return degree.text
    else :
        return None
# Thông tin giới thiệu của giảng viên
def get_introduce(soup):
    name = soup.find_all("div", class_="col-inner");
    if(len(name) > 1):
        introduce = name[1].find("p", class_="")
        if(introduce != None):
            return introduce.text
        else:
            return None
#Link đến trang soict của từng giảng viên
def get_url(soup, mydb):
    getUrl = soup.find_all("article");
    for link in getUrl:
        urlTeacher = link.find("a");
        saveData(urlTeacher['href'], mydb)

# Lấy tất cả những nghiên cứu mà giảng viên quan tâm
def get_research(soup, name):
    str = ""
    array = []
    if(name != None):
        if(soup.find("div", class_="col-inner") != None):
            researches = soup.find("div", class_="col-inner").find_all("ul")
            for research in researches:
                for research in research.find_all("li") :
                    array.append(research.text)
        array = list( set(array) )
        str = "#".join(array)
    return str

if __name__ == '__main__':
    # get_url(soup);
    get_URL(mydb)