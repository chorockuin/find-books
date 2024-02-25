import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from datetime import datetime
import re
import pandas as pd

class Book:
    def __init__(self, title, release, authors, publishers, url):
        self.contents = {"title": title, "release": release, "authors": authors, "publishers": publishers}
        self.contents["created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.url = url

def read_book_template_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        book_template = file.readlines()
    return book_template

def write_book_file(book_template, book, file_path):
    for i, line in enumerate(book_template):
        for k, v in book.contents.items():
            if line.startswith(f"{k}:"):
                if isinstance(v, list):
                    content_string = ""
                    for item in v:
                        content_string += "\n"
                        content_string += f"  - {item}"
                    book_template[i] = f"{k}: {content_string}\n"
                else:
                    content_string = v
                    book_template[i] = f"{k}: {content_string}\n"
        if line.startswith("# references"):
            book_template[i] = "# references\n" + "- " + book.url
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(book_template)

def main():
    # book_template = read_book_template_file("book.md")
    # book = Book("처음 배우는 암호화(Serious Cryptography)", "2018", ["세바스찬 라시카", "바히드 미자리리"], ["길벗"], "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=267869464")
    # write_book_file(book_template, book, "test.md")

    publishers = {
        "길벗": "663",
        "디지털북스": "7635",
        "미래의창": "8609",
        "비제이퍼블릭": "39721",
        # "스노우북": "",
        "에이콘": "7509",
        "위키북스": "20415",
        "이레미디어": "13913",
        "인사이트": "10799",
        "정보문화사": "4755",
        "제이펍": "33202",
        "지&선": "22111",
        "책만": "286290",
        "책읽는수요일": "58631",
        "프로텍미디어": "173386",
        "한빛미디어": "6555",
        "이지스퍼블리싱": "48022",
        "영진닷컴": "3853",
        "프리렉": "8202",
    }

    data = {
        "title": [],
        "release": [],
        "publisher": [],
        "url": []
    }

    for k, v in publishers.items():
        url = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&KeyRecentPublish=0&PublisherSearch=%40" + v + "&OutStock=0&ViewType=Detail&SortOrder=5&CustReviewCount=0&CustReviewRank=0&KeyWord=&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&ViewRowCount=50&SuggestKeyWord=&page=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for book_box in soup.find('div', id='Search3_Result').find_all('div', class_='ss_book_box'):
            book = book_box.find('div', class_='ss_book_list')

            title_obj = book.find('a', class_='bo3')
            url = title_obj['href']
            title = title_obj.text

            li_tags = book.find_all('li')
            for li in li_tags:
                if "(지은이)" in li.text:
                    authors = li.text.split("(지은이)")[0]
                    authors = authors.split(",")
                    authors = [author.strip() for author in authors]
                    release = re.search(r'(\d{4})년', li.text).group(1)
            data["title"].append(title)
            data["release"].append(release)
            data["publisher"].append(k)
            data["url"].append(url)
            print(authors)
            print("----------------------------")

    df = pd.DataFrame(data)
    df.to_excel('test.xlsx', index=False, engine='openpyxl')
main()