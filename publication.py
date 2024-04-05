import csv
import pandas as pd

class Publication:
    list_separator = '&&'
    
    def __init__(self, title: str='', abstract: str='', release: str='', authors: list[str]=[], publishers: list[str]=[], url: str='') -> None:
        self.title = title
        self.abstract = abstract
        self.release = release
        self.authors = authors
        self.publishers = publishers
        self.url = url
        
    def __str__(self) -> str:
        return f"""
        title: {self.title}\n
        abstract: {self.abstract}\n
        release: {self.release}\n
        authors: {Publication.list_separator.join(self.authors)}\n
        publishers: {Publication.list_separator.join(self.publishers)}\n
        url: {self.url}\n"""
    
def get_latest_publication_release(pubs: list[Publication]) -> str:
    return max(pub.release for pub in pubs)

def sort_publications(pubs: list[Publication]) -> list[Publication]:
    return sorted(pubs, key=lambda pub: (pub.publishers, pub.release))

def merge_publications(pubs_a: list[Publication], pubs_b: list[Publication]) -> list[Publication]:
    return sort_publications({pub.title: pub for pub in (pubs_a + pubs_b)}.values())

def remove_publications(pubs: list[Publication], titles_removed: str) -> list[Publication]:
    return sort_publications([pub for pub in pubs if pub.title not in titles_removed])

def create_publications_df(pubs: list[Publication]) -> pd.DataFrame:
    return pd.DataFrame([{
            'select': False,
            'number': str(i + 1),
            'title': pub.title,
            'abstract': pub.abstract,
            'release': pub.release,
            'publishers': ', '.join(pub.publishers),
            'url': pub.url,
            'authors': ', '.join(pub.authors),
        } for i, pub in enumerate(pubs)])

def write_publications_to_csv_file(pubs: list[Publication], csv_file_path: str) -> None:
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(list(vars(Publication()).keys()))
        for pub in pubs:
            writer.writerow([pub.title, pub.abstract, pub.release, Publication.list_separator.join(pub.authors), Publication.list_separator.join(pub.publishers), pub.url])

def read_publications_from_csv_file(csv_file_path: str) -> list[Publication]:
    pubs = []
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                pubs.append(Publication(row[0], row[1], row[2], row[3].split(Publication.list_separator), row[4].split(Publication.list_separator), row[5]))
    except Exception as e:
        print(f"{e}")
    return pubs