import urllib
import requests
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup

session = requests.Session()
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
        doc = bs.find_all('span', {'class': 'image'})
        # doc = bs.find_all({'p'})
        # doc = bs.find_all('span', {'class': 'toctext'})
    except AttributeError as e:
        return None
    return doc


title = urllib.parse.quote(input("검색할 단어를 입력해주세요. \n"))
Url_title = (Url + str(title).replace("'", ""))

soup = getdoc(Url_title)
if title == None:
    print("Title could not be found")
else:
    for docs in soup:
        print(docs.get_text())
