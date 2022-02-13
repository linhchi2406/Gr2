#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import re

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

if __name__ == '__main__':
    mydb = pymysql.connect(
        host="localhost",
        port =3308,
        user="root",
        password="linhchi",
        db="soict"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT fullname FROM soict")

    myresult = mycursor.fetchall()

    
    for x in myresult:
    #     if (str(x[0]) != "None"):
    #         name = str(x[0]).split(' ')[1]
    #         if (len(str(x[0]).split(' ')) > 2) :
    #             for num in range(2, len(str(x[0]).split(' '))):
    #                 name = name + " " + str(x[0]).split(' ')[num]
    #         print("-".join(name.split(' ')) + " "+ str(x[0]).split(' ')[0] )
           
        # print(x[0])  
        print(no_accent_vietnamese(str(x[0])))
        # print(no_accent_vietnamese(len(str(x[0])).split(' ')))
        # print(no_accent_vietnamese(str(x[0])).split(' ')[0])
        # print("-".join(str(x[0]).split(' ')))
        
        # for array in str(x[0]).split(' '):    
        #     print(len(str(x[0]).split(' ')))
    # print(no_accent_vietnamese("Welcome to Vietnam !"))
    # print(no_accent_vietnamese("VIỆT NAM ĐẤT NƯỚC CON NGƯỜI"))
    # https://dblp.uni-trier.de/search?q=Do+Ba+Lam