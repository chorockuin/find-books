import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas as pd
import publishers

class Book:
    def __init__(self, title, release, authors, publishers, url):
        self.contents = {"title": title, "release": release, "authors": authors, "publishers": publishers}
        self.contents["created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.url = url

def read_template_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        book_template = file.readlines()
    return book_template

def write_book_to_md_file(template_md_file_path, book, md_file_path):
    template = read_template_md_file(template_md_file_path)
    for i, line in enumerate(template):
        for k, v in book.contents.items():
            if line.startswith(f"{k}:"):
                if isinstance(v, list):
                    content_string = ""
                    for item in v:
                        content_string += "\n"
                        content_string += f"  - {item}"
                    template[i] = f"{k}: {content_string}\n"
                else:
                    content_string = v
                    template[i] = f"{k}: {content_string}\n"
        if line.startswith("# references"):
            template[i] = "# references\n" + "- " + book.url
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.writelines(template)

def find_book(publishers, last_YYMM):
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
                    release = re.search(r'(\d{4})년 (\d{1,2})월', li.text)
                    YY = f"{release.group(1)}"
                    MM = f"{release.group(2).zfill(2)}"
                    if int(YY+MM) >= last_YYMM:
                        release = f"{YY}.{MM}"
                        data["title"].append(title)
                        data["release"].append(release)
                        data["publisher"].append(k)
                        data["url"].append(url)
                        print(f"{k}: {title} {release}")

    df = pd.DataFrame(data)
    df.to_excel('test.xlsx', index=False, engine='openpyxl')

def main():
    find_book(publishers.publishers, 202308)
    # book_template = read_book_template_file("book.md")
    # book = Book("처음 배우는 암호화(Serious Cryptography)", "2018", ["세바스찬 라시카", "바히드 미자리리"], ["길벗"], "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=267869464")
    # write_book_file(book_template, book, "test.md")

main()