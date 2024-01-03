from typing import List, Optional
from collections import OrderedDict
import re
import requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup

from news_collector.interfaces import NewsCollector


class BBCNewsCollector(NewsCollector):
    '''
    TODO
    '''
    BASE_URL = "https://www.bbc.com"
    START_URL = BASE_URL + "/news/world/middle_east"
    LIVE_NEWS_LINK_PATTERN = "news/live"

    def __get_live_news_url(self) -> Optional[str]:
        """
        TODO
        :return:
        """
        res = requests.get(self.START_URL)
        if res.status_code == 200:
            html = BeautifulSoup(res.text, 'html.parser')
            a = html.find('a', href=re.compile(self.LIVE_NEWS_LINK_PATTERN))
            if a is not None:
                return self.BASE_URL + a.get("href")
        return None
    
    def collect(self, news_url=None) -> List[Optional[OrderedDict]]:
        """
        TODO
        :return: List of the collected posts. Every post is dictionary
        """
        output = []

        live_news_url = self.__get_live_news_url() if news_url is None else news_url
        if live_news_url is None:
            return output

        res = requests.get(live_news_url)
        html = BeautifulSoup(res.text, 'html.parser')

        for article in html.find_all('article'):
            id = article.get("id") # e.g. post_657ab19d69d486126e9421a4
            if id is not None and len(splitted_id := id.split("_")) == 2:
                post_id = splitted_id[1]
            else:
                continue

            url_block = article.find('input', class_=re.compile('lx-share-tools__copylink-box'))
            if url_block is not None:
                post_url =  live_news_url + url_block.get('value')
            else:
                post_url = live_news_url

            title_block = article.find('span', class_=re.compile('header-text'))
            post_title = title_block.text if title_block is not None else title_block

            time_block = article.find('time')
            time_block = time_block.find('span', class_=re.compile("qa-post-auto-meta"))
            if time_block is not None:
                datetime_parts = time_block.string.split()
                today = datetime.now(timezone.utc).date()
                if len(datetime_parts) == 1:
                    datetime_str = f"{today.year}-{today.month}-{today.day}T{datetime_parts[0]}:00"
                    post_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
                else:
                    month = datetime.strptime(datetime_parts[2], '%b').month
                    day = datetime_parts[1]
                    datetime_str = f"{today.year}-{month}-{day}T{datetime_parts[0]}:00"
                    post_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
            else:
                post_datetime = None

            contributor_block = article.find('div', class_=re.compile('contributor-body'))
            if contributor_block is not None:
                name = contributor_block.find('p', class_=re.compile('contributor-name'))
                name = name.string if name else ''
                role = contributor_block.find('p', class_=re.compile('contributor-role'))
                role = role.string if role else ''
                post_author = f"{name};{role}"
            else:
                post_author = None

            text_block = article.find('div', class_=re.compile('post-body'))
            text = []
            if text_block is not None:
                text = [p_block.text if p_block is not None else '' for p_block in text_block.find_all('p')]

            text = '\n'.join(text)

            if text:
                post = OrderedDict()
                post['id'] = post_id
                post['url'] = post_url
                post['title'] = post_title
                post['datetime'] = post_datetime.strftime('%Y-%m-%dT%H:%M:%S') if post_datetime else None
                post['author'] = post_author
                post['text'] = text
                post['provider'] = 'BBC'
                post['source'] = 'site-live-news'

                output.append(post)
        return output

    def collect_all_pages(self, main_url) -> List[Optional[OrderedDict]]:
        """
        TODO
        :param main_url:
        :return:
        """
        output = []
        res = requests.get(main_url)
        html = BeautifulSoup(res.text, 'html.parser')
        total_page_block = html.find('span', class_=re.compile('qa-pagination-total-page-number'))
        if total_page_block is not None:
            total_pages = int(total_page_block.string)
        else:
            total_pages = 1

        for page in range(1, total_pages + 1):
            news_url = f"{main_url}/page/{page}"
            output += self.collect(news_url)

        return output


if __name__ == "__main__":
    main_url = "https://www.bbc.com/news/live/world-middle-east-67847427"
    bbc = BBCNewsCollector()
    result = bbc.collect_all_pages(main_url)