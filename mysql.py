from abc import abstractclassmethod
import pymysql

mydb = pymysql.connect(
  host="localhost",
  port =3308,
  user="root",
  password="linhchi",
  db="test"
)

def doQuery( conn ):
  cur = conn.cursor()
  cur.execute("SELECT email FROM users;")
  for email in cur.fetchall():
        print(email)

doQuery(mydb)
mydb.close()
import json

s = 'hello Đạt'
with open('test.json', 'w', encoding='utf8') as fw:.
  json.dump(s, fw, indent = 4, ensure_ascii= False)