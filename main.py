import urllib
import requests
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

conn = pymysql.connect(host="192.168.0.109", user="root", password="1111", db="pythondb", charset="utf8")
cursor = conn.cursor()

url = "https://ko.wikipedia.org/wiki/"

word = urllib.parse.quote(input("검색할 단어를 입력해주세요. \n"))
Url_word = url + str(word).replace("'", "")
input_time.insert(1, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

cursor.execute(
    f"INSERT INTO ta_table (url_key ,url, stat, input_date) VALUES (\"{word}\", \"{Url_word}\", 'N', \"{input_time}\")"
)
conn.commit()

check = "SELECT stat FROM ta_table"
cursor.execute(check)
conn.commit()
row = cursor.fetchall()
print(len(row))
print(row)

if len(row) == 1:
    row_num = 1
elif len(row) >= 1:
    row_num = len(row) - 1

loopbreak = True
for i in (0, row_num):
    if row[i][0] == 'N':
        check = "SELECT url_key FROM scrap_table"
        cursor.execute(check)
        conn.commit()
        row = cursor.fetchall()
        for j in row:
            print(j)
            if word == j[0]:
                cursor.execute(
                    f"UPDATE ta_table set stat = 'I'"
                )
                cursor.execute(
                    f"UPDATE scrap_table set try = try + 1"
                )

                print("중복 키값 진행")
                content = scrapeWiki(Url_word)
                print('문서명: {}'.format(content.title))
                print('URL: {}'.format(content.url))

                tags = content.body.replace('"', "")

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
                loopbreak = False
                break
        if loopbreak == False:
            break


        cursor.execute(
            f"UPDATE ta_table set stat = 'I'"
        )
        cursor.execute(
            f"INSERT INTO scrap_table (url_key, connect_type, try,  input_date) VALUES (\"{word}\",'TA', 1, \"{input_time}\")"
        )
        check = "SELECT try FROM scrap_table"
        cursor.execute(check)
        conn.commit()
        row = cursor.fetchone()

        print("정상 진행")
        content = scrapeWiki(Url_word)
        print('문서명: {}'.format(content.title))
        print('URL: {}'.format(content.url))
        tags = content.body.replace('"', "")

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

