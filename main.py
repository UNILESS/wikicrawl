import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept": "text_html,application_xhtml+xml,application_xml;q=0.9,image_webp,**/**;q=0.8",
    "Connection": "close"
}
Url = "https://ko.wikipedia.org/wiki/"

title = input("검색할 단어를 입력해주세요. ")

Url_title = Url + title

soup = BeautifulSoup(session.get(Url_title, headers=headers).content, "html.parser")