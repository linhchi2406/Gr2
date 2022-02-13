import requests
import json
import csv
from bs4 import BeautifulSoup
import pymysql
import re
import math
from collections import Counter
mydb = pymysql.connect(
  host="localhost",
  port =3308,
  user="root",
  password="linhchi",
  db="soict"
)

url ="https://dblp.uni-trier.de/search?q="
link = "https://dblp.uni-trier.de/search?q=Nguyen+Khanh+Van"
# Kiểm tra độ tương đồng giữa 2 string
Word = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = Word.findall(text)
     return Counter(words)

# Chuyển sang dạng không có dấu
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
            get_URL(link, id, name)
        
# Lấy Các URL có thể lấy dữ liệu của từng người
def get_URL(link, id, name):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    ul = soup.find_all("ul", class_="result-list")
    if (ul):
        if (ul[0]):
            urls = ul[0].find_all("a");
            if(len(getCoauthorSchoolar(id)) == 0):
                if compareName(urls[0], name) == 1 :
                    checkTeacher(id, urls[0]['href'])
            else :
                for url in urls:
                    if (compareName(url, name) == 1) :
                        name = url.find("span").text
                        checkTeacher(id, url['href'])
                if (len(ul)>1) :
                    urls = ul[1].find_all("a");
                    for url in urls:
                        if compareName(url, split_name(name)) == 1 :
                            checkTeacher(id, url['href'])
                        # print(getCoauthorSchoolar(id))
                    # getUrlExport(urls[0]['href'])
    print("=======")
#So sanh ten cua giang vien
def compareName(url, name):
    if (set(name) == set(split_name(url.find("span").text))):
        return 1
    return 0
# Lấy link export từng bài báo
def getUrlExport(link):
    print(link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find("li", class_="export drop-down")
    link = links.find("a")['href']
    getContent(link)
#Lấy dữ liệu từng bài báo
def getContent(link):
    array = []
    print(link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    contents = soup.find_all("pre", class_="verbatim select-on-click")
    for content in contents:
        content = content.text
        array.append(content)
    return array
# Tach ten de so sanh, luu DB
def split_name(name):
    array = []
    for test in name.split("-") :
        for test1 in test.split(" "):
            array.append(test1)
    return array
 # Luu dong tac gia
def getauthor(str):
    array = []
    strs = str.split(',')
    for str1 in strs:
        r1 = re.findall(r"author",str1)
        if (len(r1)>0) :
            str1 = str1.replace('-', ' ').replace('{', '').replace('}', '').replace("author    = ", '').split("and")
            for s in str1:
                array.append(s.strip("\n").strip(" "))
    return array
#Lấy tên của bài báo, dự án nghiên cứu
def getTitle(str):
    array = []
    strs = str.split(',')
    for str1 in strs:
        r1 = re.findall(r"title     =",str1)
        if (len(r1)>0) :
            str1 = str1.replace('{', '').replace('}', '').replace("title     =", '').replace("\n", "").split()
            array.append(' '.join(str1))
    return array
#Lấy năm của từng bài báo
def getYear(str):
    year = 0
    strs = str.split(',')
    for str1 in strs:
        r1 = re.findall(r"year",str1)
        if (len(r1)>0) :
            year = str1.replace('{', '').replace('}', '').replace("year      = ", '').replace("\n", "").strip(" ")
    return year

# Lay tat ca cac dong tac gia cua trang schoolar 
def getCoauthorSchoolar(id) :
    array = []
    cur = mydb.cursor()
    sql = "SELECT name FROM coauthors where soict_id = %s"
    val = [id]
    cur.execute(sql, val)
    records = cur.fetchall()
    mydb.commit()
    for record in records:
        array.append(no_accent_vietnamese(record[0]))
    return array

def checkTeacher(id, link):
    array = getCoauthorSchoolar(id)
    contents = getUrlExport(link)
    # print(id, contents)
    
    # for content in contents :
    #     print(getauthor(content.text))
    
#Lưu dữ liệu vào bảng danh sách các nghiên cứu
def saveTitle(val) :
    cur = mydb.cursor()
    sql = "INSERT INTO titles (soict_id, title, year) VALUES (%s, %s, %s)"
    cur.execute(sql, val)
    mydb.commit()
#Lưu dữ liệu vào bảng đồng tác giả
def saveCoauthor(val) :
    cur = mydb.cursor()
    sql = "INSERT INTO titles (soict_id, title, year) VALUES (%s, %s, %s)"
    cur.execute(sql, val)
    mydb.commit()
if __name__ == '__main__':
    # get_url(soup);
    getURL(mydb, url)
