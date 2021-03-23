import urllib
import requests
from html_table_parser import parser_functions as parser
from bs4 import BeautifulSoup
import pymysql
import datetime


class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body


def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')


def scrapeWiki(url):
    bs = getPage(url)
    title = bs.find('h1').text
    lines = bs.select('p')
    '''table = bs.select('table')
    for i in range(0, len(table)):
        tables = parser.make2d(table[i])
        print(tables)'''
    body = '\n'.join([line.text for line in lines])
    # tables_result = '\n'.join([tables.text for tables in tables])
    return Content(url, title, body)

input_time = []


conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="pythonDB", charset="utf8")
cursor = conn.cursor()

url = "https://ko.wikipedia.org/wiki/"

word = urllib.parse.quote(input("검색할 단어를 입력해주세요. \n"))
Url_word = url + str(word).replace("'", "")
print(Url_word)
input_time = list(reversed(input_time))

cursor.execute(
    "INSERT INTO ta_table (url, stat, input_date) VALUES (%s, %s ,%s);", (Url_word, 'N', input_time)
)

cursor.execute(
    "SELECT @ROWNUM:=@ROWNUM+1, A.* FROM ta_table A, (SELECT @ROWNUM:=0) R;"
)

conn.commit()

content = scrapeWiki(Url_word)
print('문서명: {}'.format(content.title))
print('URL: {}'.format(content.url))
print(content.body)

# DB 저장

