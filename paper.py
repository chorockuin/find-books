import datetime
import re

import bs4
import googletrans

import webdriver
import publication

def get_dates_since(since_year, since_month, since_day):
    start_date = datetime.datetime(int(since_year), int(since_month), int(since_day))
    end_date = datetime.datetime.now()
    dates = []
    while start_date <= end_date:
        dates.append(start_date.strftime('%Y-%m-%d'))
        start_date += datetime.timedelta(days=1)
    return dates

def get_arxiv_paper(chrome, url, papers_file_path):
    webdriver.get(chrome, url)
    soup = bs4.BeautifulSoup(chrome.page_source, 'html.parser')
    
    translater = googletrans.Translator()
    
    title = soup.find('h1', class_='title mathjax')
    title.span.decompose()
    title = title.get_text(strip=True)
    # title = translater.translate(title, dest='ko').text
    
    abstract = soup.find('blockquote', class_='abstract mathjax')
    abstract.span.decompose()
    abstract = abstract.get_text(strip=True)
    abstract = translater.translate(abstract, dest='ko').text
    
    authors = soup.find('div', class_='authors')
    authors = [a.get_text(strip=True) for a in authors.find_all('a')]

    release = soup.find('div', class_='dateline')
    release = release.get_text(strip=True)
    release = release.strip('[]')
    release = release.split(' ')
    release = release[2] + ' ' + release[3] + ' ' + release[4]
    release = datetime.datetime.strptime(release, '%d %b %Y').strftime('%Y.%m.%d')
        
    publishers = ['arxiv']

    new_paper = publication.Publication(title, abstract, release, authors, publishers, url)
    old_papers = publication.read_publications_from_csv_file(papers_file_path)
    publication.write_publications_to_csv_file(publication.merge_publications(old_papers, [new_paper]), papers_file_path)
    return new_paper
    
def get_arxiv_paper_url_from_huggingface_paper_page(chrome, huggingface_paper_page_url):
    webdriver.get(chrome, huggingface_paper_page_url)
    arxiv_paper_url = bs4.BeautifulSoup(chrome.page_source, 'html.parser').find('a', class_='btn inline-flex h-9 items-center')['href']
    return arxiv_paper_url

def get_huggingface_paper_page_urls(chrome, since_date):
    webdriver.get(chrome, 'https://huggingface.co/papers?date=' + since_date)
    webdriver.wait_by_xpath(chrome, '/html/body/div/main/div[2]/section/div[2]')
    a_tags = bs4.BeautifulSoup(chrome.page_source, 'html.parser').find_all('a')
    hrefs = [a_tag.get('href') for a_tag in a_tags if a_tag.get('href') is not None]
    paper_page_hrefs = set(filter(re.compile(r'/papers/\d{4}\.\d{5}$').match, hrefs))
    return ['https://huggingface.co' + paper_page_href for paper_page_href in paper_page_hrefs]

def search_papers_from_huggingface(chrome, since_date: str, papers_file_path: str):
    return [get_arxiv_paper(chrome, get_arxiv_paper_url_from_huggingface_paper_page(chrome, hugginface_paper_page_url), papers_file_path) for hugginface_paper_page_url in get_huggingface_paper_page_urls(chrome, since_date)]

def get_arxiv_paper_urls_from_top_llm_papers_of_the_week_page(chrome, page_url):
    webdriver.get(chrome, page_url)
    a_tags = bs4.BeautifulSoup(chrome.page_source, 'html.parser').find_all('a')
    hrefs = [a_tag.get('href') for a_tag in a_tags if a_tag.get('href') is not None]
    hrefs = [href for href in hrefs if 'arxiv.org' in href]
    arxiv_paper_urls = ['https://arxiv.org/abs/' + re.search(r'\d{4}\.\d{5}', href).group() for href in hrefs]
    return arxiv_paper_urls

def search_papers_from_top_llm_papers_of_the_week(chrome, since_date, papers_file_path):
    def is_since_date(since_date, page_info):
        date = page_info['date'].split(' ')
        date = datetime.datetime.strptime(date[6].replace(',', '') + ' ' + date[5] + ' ' + date[7], '%d %b %Y').strftime('%Y-%m-%d')
        if since_date <= date:
            return True
        return False
    papers = []
    webdriver.get(chrome, 'https://corca.substack.com/archive?sort=new')
    a_tags = bs4.BeautifulSoup(chrome.page_source, 'html.parser').find_all('a')
    page_infos = [{'date': a_tag.get_text(strip=True), 'href': a_tag.get('href')} for a_tag in a_tags if a_tag.get('href') is not None]
    page_infos = [page_info for page_info in page_infos if 'Vol.' in page_info['date']]
    page_infos = [page_info for page_info in page_infos if is_since_date(since_date, page_info)]
    for page_info in page_infos:
        arxiv_paper_urls = get_arxiv_paper_urls_from_top_llm_papers_of_the_week_page(chrome, page_info['href'])
        for arxiv_paper_url in arxiv_paper_urls:
            papers.append(get_arxiv_paper(chrome, arxiv_paper_url, papers_file_path))
    return papers

def search_papers(papers_file_path: str, since_year: str, since_month: str, since_day: str) -> list[publication.Publication]:
    papers = []
    chrome = webdriver.open_chrome()
    since_dates = get_dates_since(since_year, since_month, since_day)
    for since_date in since_dates:
        papers += search_papers_from_huggingface(chrome, since_date, papers_file_path)
        papers += search_papers_from_top_llm_papers_of_the_week(chrome, since_date, papers_file_path)
    webdriver.close_chrome(chrome)
    return papers