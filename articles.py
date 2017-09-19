import json
from transliterate import translit
from datetime import date
import os.path
import re


def save_article(header, signature, body, filename, token):
    article = {'header': header, 'signature': signature,
               'body': body, 'token': token}
    with open('articles/%s.json' % filename,
              mode='w', encoding='utf-8') as article_file:
        json.dump(article, article_file)
    return


def get_filename(text):
    text = re.sub('[./*!@#$?`]', '', text)
    text = text.strip()
    text = text.replace(" ", "-")
    now_date = date.today()
    url = '%s-%d-%d' % (translit(text[:15], 'ru', reversed=True),
                        now_date.day,
                        now_date.month)
    file_counter = 0
    new_url = url
    while os.path.exists('articles/%s.json' % new_url):
        file_counter += 1
        new_url = "%s-%d" % (url, file_counter)
    return new_url


def load_article(filename):
    try:
        with open('articles/%s.json' % filename) as article_file:
            article_data = json.load(article_file)
        article = dict()
        article['header'] = article_data['header']
        article['signature'] = article_data['signature']
        article['body'] = article_data['body']
        article['token'] = article_data['token']
        return article
    except FileNotFoundError:
        return None
