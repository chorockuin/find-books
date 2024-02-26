import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import pandas
import publishers
import csv

class Book:
    def __init__(self, title, release, authors, publishers, url):
        self.contents = {'title': title, 'release': release, 'authors': authors, 'publishers': publishers}
        self.contents['created'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.url = url
    
    def __str__(self):
        return f"title: {self.contents['title']}\nrelease: {self.contents['release']}\nauthors: {':'.join(self.contents['authors'])}\npublishers: {':'.join(self.contents['publishers'])}\nurl: {self.url}\n"

def read_template_md_file(template_md_file_path):
    with open(template_md_file_path, 'r', encoding='utf-8') as file:
        template_md = file.readlines()
    return template_md

def write_book_to_md_file(template_md, book, md_file_path):
    for i, line in enumerate(template_md):
        for k, v in book.contents.items():
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
        
def fix_title(title):
    return title

def write_books_to_md_file(template_md, books, md_dir):
    for book in books:
        md_file_path = md_dir + '/' + fix_title(book.contents['title'])
        write_book_to_md_file(template_md, book, md_file_path)
        
def write_books_to_csv_file(books, csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'release', 'authors', 'publishers', 'url'])
        for book in books:
            writer.writerow([book.contents['title'], book.contents['release'], ':'.join(book.contents['authors']), ':'.join(book.contents['publishers']), book.url])
            
def read_books_from_csv_file(csv_file_path):
    books = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title = row[0]
            release = row[1]
            authors = row[2].split(":")
            publishers = row[3].split(":")
            url = row[4]
            books.append(Book(title, release, authors, publishers, url))
    return books

def find_books(publishers, lastest_release_year_month):
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
                    if int(year + month) >= lastest_release_year_month:
                        release = f'{year}.{month}'
                        books.append(Book(title, release, authors, [pub_name], url))
    return books

def main():
    # books = find_books(publishers.publishers, 202308)
    
    # write_books_to_csv_file(books, 'books.csv')
    books = read_books_from_csv_file('books.csv')
    for book in books:
        print(book)
    
    
    # df = pandas.DataFrame(data)
    # df.to_excel('test.xlsx', index=False, engine='openpyxl')

    
    # book_template = read_book_template_file('book.md')
    # book = Book('처음 배우는 암호화(Serious Cryptography)', '2018', ['세바스찬 라시카', '바히드 미자리리'], ["길벗"], "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=267869464")
    # write_book_file(book_template, book, "test.md")

main()