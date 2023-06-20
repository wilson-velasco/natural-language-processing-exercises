import requests
from bs4 import BeautifulSoup
import os

def get_blog_articles(urls):
    '''Takes in a list of URLs and produces a list of dictionaries that includes the blog's title and main body content.'''

    #Initiate dictionary of entries
    code_up_dict = []

    #To allow access to pages
    header = {"User-Agent": "Chrome/91.0.4472.124"}

    #Cycle through the URLs
    for url in urls:
        response = requests.get(url, headers = header)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Get title
        title = soup.title.string
        
        #Get content
        contents = soup.find('div', class_='entry-content').text.replace('\n', ' ')
        
        dict_entry = {'url': url
                    ,'title': title
                    ,'content': contents}
            
        code_up_dict.append(dict_entry)

    return code_up_dict

def get_news_articles(categories=['business', 'sports', 'technology', 'business']):
    '''Takes in a list of categories (default is Business, Sports, Technology, and Business).
    
    Outputs a list of dictionaries to include the title and content of the news article, as well as the category.'''

    #Initiate list
    inshorts_dict = []

    for categorie in categories:
        url = f'https://inshorts.com/en/read/{categorie}'
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup.find_all('div', class_='news-card z-depth-1'):
            title = element.find('span', itemprop='headline').text
            content = element.find('div', itemprop='articleBody').text.replace('\n', '')
            category = categorie
            
            dict_entry = {'title': title
                        ,'content': content
                        ,'category': category}
            
            inshorts_dict.append(dict_entry)

    return inshorts_dict