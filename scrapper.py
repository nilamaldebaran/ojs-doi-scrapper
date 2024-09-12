import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

urls = [
    # Issue URLs
    "url1",
    "url2",
    "url3"
]

articles = []

for url in urls:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        for article in soup.find_all('div', class_='obj_article_summary'):
            title_tag = article.find('h3', class_='title').find('a')
            title = title_tag.text.strip()
            link = urljoin(url, title_tag['href'])  
            
            doi_tag = article.find('div', class_='doiInSummary')
            doi = doi_tag.find('a').text.strip() if doi_tag else 'DOI not found'
            
            articles.append([title, link, doi])
    else:
        print(f"Failed request with status code {response.status_code} for URL: {url}")

df = pd.DataFrame(articles, columns=["Title", "Link", "DOI"])

df.to_csv('articles.csv', index=False, sep=';')

print("Writen successfully to: articles.csv")
