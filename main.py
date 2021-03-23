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
process_time = []

conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="pythonDB", charset="utf8")
cursor = conn.cursor()

url = "https://ko.wikipedia.org/wiki/"

word = urllib.parse.quote(input("검색할 단어를 입력해주세요. \n"))
Url_word = url + str(word).replace("'", "")
print(Url_word)
input_time.insert(1, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

cursor.execute(
    f"INSERT INTO ta_table (url, stat, input_date) VALUES (\"{Url_word}\", 'N', \"{input_time}\")"
)
conn.commit()

check = "SELECT * FROM ta_table"
cursor.execute(check)
conn.commit()

row = cursor.fetchone()

count = cursor.execute(
    f"SELECT COUNT(stat) FROM ta_table"
)

for i in (0, count):
    # count 열 손 봐야됨
    if row[3] == 'N':
        cursor.execute(
            f"UPDATE ta_table set stat = 'I'"
        )
        cursor.execute(
            f"INSERT INTO scrap_table (connect_type, try,  input_date) VALUES ('TA', 1, \"{input_time}\")"
        )
        print("진행")
        content = scrapeWiki(Url_word)
        print('문서명: {}'.format(content.title))
        print('URL: {}'.format(content.url))

        tags = content.body.replace('"', "")
        print(tags)
        # DB 저장
        process_time.insert(1, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        process_time = process_time[0].replace('"', '')
        cursor.execute(
            f"update ta_table set result_tag = \"{tags}\", process_date = \"{process_time}\", stat = 'Y'"
        )
        conn.commit()
        cursor.execute(
            f"UPDATE scrap_table set process_date = \"{process_time}\""
        )
        conn.commit()

        check1 = "SELECT * FROM scrap_table"
        cursor.execute(check1)
        conn.commit()

        row = cursor.fetchone()

        if row[7] >= 1:
            cursor.execute(
                f"UPDATE scrap_table set try = {row[7] + 1} "
            )


