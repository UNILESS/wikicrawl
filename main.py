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
print('Title: {}'.format(content.title))
print('URL: {}'.format(content, Url_word))
print(content.body)


'''session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept": "text_html,application_xhtml+xml,application_xml;q=0.9,image_webp,**/**;q=0.8",
    "Connection": "close"
}
Url = "https://ko.wikipedia.org/wiki/"


def getdoc(url):
    try:
        soup = BeautifulSoup(urlopen(Url_title).read(), "html5lib")
    except HTTPError as e:
        print(e)
    try:
        bs = BeautifulSoup(urlopen(Url_title).read(), "html5lib")
        doc = bs.select('body')
        # doc = bs.find_all({'p'})
        # doc = bs.find_all('span', {'class': 'toctext'})
    except AttributeError as e:
        return None
    return doc


title = urllib.parse.quote(input("검색할 단어를 입력해주세요. \n"))
Url_title = (Url + str(title).replace("'", ""))
soup = getdoc(Url_title)

if title is None:
    print("Title could not be found")
else:
    for docs in soup:
        print(docs.get_text())
'''