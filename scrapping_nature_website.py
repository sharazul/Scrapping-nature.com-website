import requests
from bs4 import BeautifulSoup
import re
import os


# function checks the type of article i,e News,Research Articles etc
def check_article_type(each_article):
    get_all_span = each_article.find_all('div', class_="c-card__section c-meta")
    for filter_span in get_all_span:
        type_ws = filter_span.find('span', {"data-test": "article.type"})
        # "data-test": "article.type" contains the article type i,e News,Research Articles etc
        get_span_text = type_ws.find('span').text
        return get_span_text


# this function removes extra letters from title and add '_' after each word
def remove_punctuation(article_type_text, input_text, each_article):
    # compare article type here if equal then continue
    if article_type_text == input_text:
        title_text = str(each_article.a.text)
        pun1 = re.sub(r'[^\w\s]', '', title_text).split(' ')
        pun1 = [i for i in pun1 if i]
        # making a file name with the news title
        file_name = '_'.join(pun1) + '.txt'
        fetch_url = 'https://www.nature.com' + each_article.a['href']
        return [file_name, fetch_url]


def get_full_news(page_url, type_of_article):
    resp = requests.get(page_url)
    all_data = BeautifulSoup(resp.content, 'html.parser')
    all_articles = all_data.find_all('article')
    for all_div in all_articles:
        if type_of_article in ['News', 'News & Views', 'News Feature']:
            f1 = all_div.find('div', class_="c-article-body u-clearfix")
            if f1 is not None:
                content_ws = f1.text
                return content_ws
        elif type_of_article == "Research Highlight":
            find_r_article = all_div.find('div', class_="article-item__body")
            if find_r_article is not None:
                content_ws = find_r_article.text
                return content_ws
        elif type_of_article == 'Article':
            find_article_1 = all_div.find("div", class_="c-article-body")
            if find_article_1 is not None:
                find_article_2 = find_article_1.find('div', class_="c-article-section__content")
                content_ws = find_article_2.text
                return content_ws


# write content to file
def write_to_file(full_path, filename, data):
    filename = '\\' + filename
    file = open(full_path + filename, 'wb')
    file.write(data.strip().encode() + '\n'.encode())
    file.close()


# program starts from here....
page_N = int(input()) + 1
input_article_type = input()
# get current working directory
current_dir = os.getcwd()
for n in range(1, page_N):
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={n}"
    # changing directory to current working directory
    os.chdir(current_dir)
    os.mkdir(f'page_{n}')
    # Now change path to the newly created folder
    os.chdir(current_dir + '//page_{}'.format(n))
    path = os.getcwd()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fetch_all_articles = soup.find_all('article')
    for every_article in fetch_all_articles:
        article_type = check_article_type(every_article)
        get_filename_and_url = remove_punctuation(article_type, input_article_type, every_article)
        if get_filename_and_url is not None:
            # getting content from the body of article and then write it into a text file
            content = get_full_news(get_filename_and_url[1], article_type)
            write_to_file(path, get_filename_and_url[0], content)
