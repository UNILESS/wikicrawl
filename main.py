import urllib
import requests
from urllib.request import urlopen
#  from urllib.request import HTTPError
from bs4 import BeautifulSoup


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
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)


url = "https://ko.wikipedia.org/wiki/"

word = urllib.parse.quote(input("검색할 단어를 입력해주세요. \n"))
Url_word = (url + str(word).replace("'", ""))

content = scrapeWiki(Url_word)
print('문서명: {}'.format(content.title))
print('URL: {}'.format(content.url))
print(content.body)
