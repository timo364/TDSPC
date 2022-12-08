from datetime import datetime
from json import dump as json_dump
from pathlib import Path

from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
from requests import get as req_get


URL = 'https://www.pravda.com.ua/eng/rss/'
DIR = Path(__file__).parent


app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.beat_schedule = {
    'scraping': {
        'task': 'tasks.scrape',
        # Scrapes every 1 minute.
        'schedule': crontab()
    }
}


@app.task
def scrape():
    '''
    Crates `output` directory if not exists. Tries to get latest articles from
    link set in global `URL` variable. Sorts info for every article and
    generates json files under `output` dir: adds `title`, `description`,
    `source`, `published_at` and `scrapped_at` attributes.
    '''
    output_dir = DIR.joinpath('output')
    output_dir.mkdir(parents=True, exist_ok=True)
    articles = []

    try:
        response = req_get(URL)
        soup = BeautifulSoup(response.content, features='xml')
        scraped_articles = soup.findAll('item')

        for a in scraped_articles:
            article = {
                'title': a.find('title').text,
                'description': a.find('description').text,
                'source': a.find('link').text,
                'published_at': a.find('pubDate').text,
                'scrapped_at': str(datetime.now()),
            }
            articles.append(article)

        saved_at = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')

        with open(
            f'{DIR}/output/articles-{saved_at}.json', 'w') as out_file:
            json_dump(articles, out_file, indent=4)

        return saved_at

    except Exception as e:
        print(f'Exception:\n{e}')
