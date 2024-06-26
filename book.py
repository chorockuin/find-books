import requests
import re
import bs4
import publication

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
    # "영진닷컴": "3853",
    "프리렉": "8202",
    "생능북스": "436531",
    "애드앤미디어": "335898",
    # "커뮤니케이션북스": "5433",
}

def search_books(books_file_path: str, since_year: str, since_month: str, since_day: str) -> list[publication.Publication]:
    books = []
    for publisher_name, publisher_id in publishers.items():
        url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&KeyRecentPublish=0&PublisherSearch=%40' + publisher_id + '&OutStock=0&ViewType=Detail&SortOrder=5&CustReviewCount=0&CustReviewRank=0&KeyWord=&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&ViewRowCount=50&SuggestKeyWord=&page=1'
        response = requests.get(url, verify=False)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
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
                    if year + month >= since_year + since_month:
                        release = f"{year}.{month}.01"
                        old_books = publication.read_publications_from_csv_file(books_file_path)
                        new_book = publication.Publication(title, '', release, authors, [publisher_name], url)
                        publication.write_publications_to_csv_file(publication.merge_publications(old_books, [new_book]), books_file_path)
                        books.append(new_book)
    return books

def read_template_book_md_file(template_md_file_path: str) -> str:
    with open(template_md_file_path, 'r', encoding='utf-8') as file:
        template_md = file.readlines()
    return template_md

def write_book_to_book_md_file(template_md: str, book: publication.Publication, md_file_path: str) -> None:
    for i, line in enumerate(template_md):
        for k, v in book.__dict__.items():
            if line.startswith(f'{k}:'):
                if isinstance(v, list):
                    content_string = ''
                    for item in v:
                        content_string += '\n'
                        content_string += f'  - {item}'
                    template_md[i] = f'{k}: {content_string}\n'
                else:
                    content_string = v
                    template_md[i] = f'{k}: {content_string}\n'
        if line.startswith('# references'):
            template_md[i] = '# references\n' + '- ' + book.url
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.writelines(template_md)
        
def fix_title(title: str) -> str:
    return title

def write_books_to_md_file(template_md: str, books: list[publication.Publication], md_dir: str):
    for book in books:
        md_file_path = md_dir + '/' + fix_title(book.title)
        write_book_to_book_md_file(template_md, book, md_file_path)