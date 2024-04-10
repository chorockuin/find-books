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

def get_arxiv_paper(chrome, url):
    chrome.get(url)
    soup = bs4.BeautifulSoup(chrome.page_source, 'html.parser')
    
    translater = googletrans.Translator()
    
    title = soup.find('h1', class_='title mathjax')
    title.span.decompose()
    title = title.get_text(strip=True)
    title = translater.translate(title, dest='ko').text
    
    abstract = soup.find('blockquote', class_='abstract mathjax')
    abstract.span.decompose()
    abstract = abstract.get_text(strip=True)
    abstract = translater.translate(abstract, dest='ko').text
    
    authors = soup.find('div', class_='authors')
    authors = [a.get_text(strip=True) for a in authors.find_all('a')]

    release = soup.find('div', class_='dateline')
    release = release.get_text(strip=True)
    release = release.strip("[]").replace("Submitted on ", "")
    release = datetime.datetime.strptime(release, "%d %b %Y").strftime("%Y.%m.%d")
        
    publishers = ['arxiv']
    return publication.Publication(title, abstract, release, authors, publishers, url)
    
def search_huggingface_blog(chrome, since_year: str, since_month: str, since_day: str):
    papers = []
    dates = get_dates_since(since_year, since_month, since_day)
    for date in dates:
        url = 'https://huggingface.co/papers?date=' + date
        chrome.get(url)
        a_tags = bs4.BeautifulSoup(chrome.page_source, 'html.parser').find_all('a')
        hrefs = [a_tag.get('href') for a_tag in a_tags if a_tag.get('href') is not None]
        paper_href_pattern = re.compile(r'/papers/\d{4}\.\d{5}$')
        paper_hrefs = set(filter(paper_href_pattern.match, hrefs))
        for paper_href in paper_hrefs:
            paper_url = 'https://huggingface.co' + paper_href
            chrome.get(paper_url)
            arxiv_url = bs4.BeautifulSoup(chrome.page_source, 'html.parser').find('a', class_="btn inline-flex h-9 items-center")['href']
            papers.append(get_arxiv_paper(chrome, arxiv_url))
    return papers

def search_papers(since_year: str, since_month: str, since_day: str) -> list[publication.Publication]:
    papers = []
    chrome = webdriver.open_chrome()
    huggingface_papers = search_huggingface_blog(chrome, since_year, since_month, since_day)
    papers += huggingface_papers
    webdriver.close_chrome(chrome)   
    return papers