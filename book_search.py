import book
import requests
from bs4 import BeautifulSoup
import re

publishers = {
    "인사이트": "10799",
    "에이콘": "7509",
    "한빛미디어": "6555",
    "위키북스": "20415",
    "제이펍": "33202",
    "길벗": "663",
    "책만": "286290",
    "지&선": "22111",
    "디지털북스": "7635",    
    "미래의창": "8609",
    "비제이퍼블릭": "39721",
    # "이레미디어": "13913",
    "정보문화사": "4755",
    "책읽는수요일": "58631",
    "프로텍미디어": "173386",
    "이지스퍼블리싱": "48022",
    "영진닷컴": "3853",
    "프리렉": "8202",
    "생능북스": "436531",
    "애드앤미디어": "335898",
    # "커뮤니케이션북스": "5433",
}

def search_books(since_year_month: str):
    books = []
    for pub_name, pub_id in publishers.items():
        pub_url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&KeyRecentPublish=0&PublisherSearch=%40' + pub_id + '&OutStock=0&ViewType=Detail&SortOrder=5&CustReviewCount=0&CustReviewRank=0&KeyWord=&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&ViewRowCount=50&SuggestKeyWord=&page=1'
        response = requests.get(pub_url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        for book_box_element in soup.find('div', id='Search3_Result').find_all('div', class_='ss_book_box'):
            book_element = book_box_element.find('div', class_='ss_book_list')
            title_element = book_element.find('a', class_='bo3')

            title = title_element.text
            url = title_element['href']

            for li in book_element.find_all('li'):
                if '(지은이)' in li.text:
                    authors = li.text.split('(지은이)')[0].split(',')
                    authors = [author.strip() for author in authors]
                    release = re.search(r'(\d{4})년 (\d{1,2})월', li.text)
                    year = f'{release.group(1)}'
                    month = f'{release.group(2).zfill(2)}'
                    if year + month >= since_year_month:
                        release = f'{year}.{month}'
                        books.append(book.Book(title, release, authors, [pub_name], url))
    return books