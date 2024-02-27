import typing
import datetime
import csv

class Book:
    list_separator = '&&'
    
    def __init__(self, title: str, release: str, authors: typing.List[str], publishers: typing.List[str], url: str):
        self.contents = {'title': title, 'release': release, 'authors': authors, 'publishers': publishers}
        self.contents['created'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.url = url
    
    def __str__(self):
        return f"title: {self.contents['title']}\nrelease: {self.contents['release']}\nauthors: {Book.list_separator.join(self.contents['authors'])}\npublishers: {Book.list_separator.join(self.contents['publishers'])}\nurl: {self.url}\n"

def write_books_to_csv_file(books, csv_file_path):
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'release', 'authors', 'publishers', 'url'])
        for book in books:
            writer.writerow([book.contents['title'], book.contents['release'], Book.list_separator.join(book.contents['authors']), Book.list_separator.join(book.contents['publishers']), book.url])
            
def read_books_from_csv_file(csv_file_path):
    books = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title = row[0]
            release = row[1]
            authors = row[2].split(Book.list_separator)
            publishers = row[3].split(Book.list_separator)
            url = row[4]
            books.append(Book(title, release, authors, publishers, url))
    return books

def read_template_book_md_file(template_md_file_path):
    with open(template_md_file_path, 'r', encoding='utf-8') as file:
        template_md = file.readlines()
    return template_md

def write_book_to_book_md_file(template_md, book, md_file_path):
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
        write_book_to_book_md_file(template_md, book, md_file_path)
