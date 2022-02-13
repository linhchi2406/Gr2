import requests
import dryscrape
import sys
from bs4 import BeautifulSoup
import pymysql
import re
import lxml
from time import sleep
import time

mydb = pymysql.connect(
  host="localhost",
  port =3308,
  user="root",
  password="linhchi",
  db="soict"
)
arr = []

url ="https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
# tạo các URL search theo tên teacher
def getURL(mydb, url):
    id = 0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT fullname FROM soict")
    myresult = mycursor.fetchall()
    for x in myresult:
        id = id+1
        name = no_accent_vietnamese(str(x[0])).split(' ')
        link = url + "+".join(name)
        if (x[0] != "None"):
            time.sleep(2)
            print(link)
            get_URL(link, id)
        
# Lấy dữ liệu của từng giảng viên
def get_URL(link, id):
    time.sleep(1)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "lxml")
    links = soup.find_all("div", class_="gs_ai_t")
    for link in links:
        email = link.find("div", class_="gs_ai_eml").text
        if (email == 'Verified email at soict.hust.edu.vn' or email == 'Verified email at hust.edu.vn') :
            url = link.find("a")['href']
            linkTeacher = "https://scholar.google.com" + str(url)
            # getTitle(linkTeacher, id)
            # getSpecialized(linkTeacher)
            getCoAuthor(linkTeacher, id)
            # saveSpecializedSoict(linkTeacher, id)
            # saveDataSpecialized(linkTeacher, mydb)
            # saveCoAuthor(linkTeacher, id)
            print("/////////////")
        # break
#Lấy tất cả thông tin về các sản phẩm của giảng viên
def getTitle(link, id) :
    time.sleep(10)
    page =  requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    titles = soup.find_all("tr", class_="gsc_a_tr")
    cur = mydb.cursor()
    print(id)
    for title in titles:
        sql = "INSERT INTO titles (soict_id, title, year) VALUES (%s, %s, %s)"
        val = [int(id), title.find("a", class_="gsc_a_at").text,title.find("span", class_="gsc_a_h gsc_a_hc gs_ibl").text ]        
        cur.execute(sql,val)
        mydb.commit()

#lấy tất cả thông tin về đồng tác giả
def getCoAuthor(link, id):
    time.sleep(2)
    page =  requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("td", class_="gsc_a_t")
    for link in links :
        url = "https://scholar.google.com" + str(link.find("a", class_="gsc_a_at")['href'])
        print(url)
        saveCoAuthor(url, id)

def split_name(name):
    array = []
    for test in name.split("-") :
        for test1 in test.split(" "):
            array.append(test1)
    return array
  

# Lấy đồng tác giả
def saveCoAuthor(link, id) :
    time.sleep(1)
    page =  requests.get(link)
    soup = BeautifulSoup(page.content, "lxml")
    result = 0
    authors = soup.find("div", class_="gsc_oci_value").text
    authors = authors.split(", ")
    for item in authors:
        array = split_name(item)
        cur = mydb.cursor()
        sql = "SELECT * FROM coauthor where soict_id = %s"
        val = [id]
        cur.execute(sql, val)
        records = cur.fetchall()
        for record in records:
            array1 = split_name(record[2])
            if (set(array) == set(array1)):
                result = 1
                print(1)
                break
        if (result == 0):
            sql = "INSERT INTO coauthor (name, soict_id) VALUES (%s, %s)"
            val = [item, id]
            cur.execute(sql, val)
        mydb.commit()
 
#lấy tất cả thông tin về chuyên ngành nghiên cứu
def getSpecialized(soup):
    specializeds = soup.find("div", id="gsc_prf_int")
    specializeds = specializeds.find_all("a")
    array = []
    if (specializeds != None) : 
        for specialized in specializeds:
            array.append(specialized.text)
    return array
# Lưu dữ liệu chuyên ngành vào DB
def saveDataSpecialized(link, mydb):
    time.sleep(10)
    page =  requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    val = getSpecialized(soup)
    if len(val) > 0 :
        cur = mydb.cursor()
        for item in val:
            sql = "SELECT * FROM specializeds where name = %s"
            cur.execute(sql, item)
            record = cur.fetchall()
            if(len(record) == 0):
                sql = "INSERT INTO specializeds (name) VALUES (%s)"
                cur.execute(sql, item)
            mydb.commit()

# Lưu chuyên ngành và giảng viên
def saveSpecializedSoict(link, id) :
    time.sleep(2)
    page =  requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    specializeds = soup.find("div", id="gsc_prf_int")
    specializeds = specializeds.find_all("a", class_="gsc_prf_inta gs_ibl")
    for specialized in specializeds:
        cur = mydb.cursor()
        val = specialized.text
        sql = "SELECT * FROM specializeds where name = %s"
        cur.execute(sql, val)
        record = cur.fetchall()
        # print(record[0][0])
        if (len(record) != 0):
            sql = "INSERT INTO soict_specializeds (soict_id, specialized_id) VALUES (%s, %s)"
            val = [id, record[0][0]]
            cur.execute(sql, val)
        mydb.commit()


if __name__ == '__main__':
    # get_url(soup);
    getURL(mydb, url)