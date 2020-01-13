import asyncio

import db.dbkey as dbkey
import common.util as util
from tool.twitter import Twitter, TwitterError
from scraper.tag_factory import TagFactory, BSTagError

BASE_URL = 'https://virtual-youtuber.userlocal.jp/'
RANKING_URL = BASE_URL + 'document/ranking?page={}'

class RankingScraper(object):
    def __init__(self):
        pass

    def get_ranking_data(self, page):
        vtubers = []
        for p in range(page):
            factory = TagFactory(RANKING_URL.format(p + 1))
            tag = factory.tag('table', {'class':'table-ranking'})
            for tr in tag.each('tr'):
                vtuber = {}
                vtuber[dbkey.VTUBER_OFFICE_KEY] = dbkey.UNKNOWN_TEXT
                vtuber[dbkey.VTUBER_TWITTER_KEY] = dbkey.UNKNOWN_TEXT
                vtuber[dbkey.VTUBER_YOUTUBE_KEY] = dbkey.UNKNOWN_TEXT
                vtuber[dbkey.VTUBER_NAME_KEY] = tr.child('img').alt().split('(')[0]
                vtuber[dbkey.VTUBER_RANK_KEY] = tr.strong()
                vtuber['url'] = tr.url()
                vtubers.append(vtuber)
        return vtubers

    def get_detail(self, vtubers):
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread")as executor:
            for n in range(3):
                executor.submit(self._detail, vtubers[n])
        print('end=========')

    async def _detail(self, vtuber):
        print('AAAAAAAAAAAAAA')
        # 詳細ページへジャンプしてスクレイピング
        factory = TagFactory(BASE_URL + vtuber['url'])
        tag = factory.tag('div', {'class': 'box-channel-info'})
        try:
            vtuber[dbkey.VTUBER_OFFICE_KEY] = tag.child('img').alt().split('(')[0]
        except BSTagError as ex:
            print('failed to get office : {}'.format(ex.args))
            print(vtuber[dbkey.VTUBER_NAME_KEY])

        for tag in tag.each('div', {'class': 'channel-stat'}):
            params = [tag for tag in tag.text().split('\n') if tag]
            if params[0] == 'ファン数':
                vtuber[dbkey.VTUBER_FOLLOWER_KEY] = util.kanji_numeric(params[1], '人')
            if params[0] == '総再生回数':
                vtuber[dbkey.VTUBER_VIEW_KEY] = util.kanji_numeric(params[1], '回')
            if params[0] == 'Twitter':
                vtuber[dbkey.VTUBER_TWITTER_KEY] = 'https://twitter.com/' + params[1].replace('@', '')
                try:
                    twitter = Twitter(vtuber[dbkey.VTUBER_TWITTER_KEY])
                    vtuber[dbkey.VTUBER_YOUTUBE_KEY] = twitter.youtube_url()
                except TwitterError as ex:
                    print(ex)

        print('VVVVVV = {}'.format(vtuber))
