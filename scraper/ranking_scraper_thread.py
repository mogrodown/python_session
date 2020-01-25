from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

from multiprocessing import Pool

import db.dbkey as dbkey
import common.util as util
from tool.twitter import Twitter, TwitterError
from scraper.tag_factory import TagFactory, BSTagError

BASE_URL = 'https://virtual-youtuber.userlocal.jp/'
RANKING_URL = BASE_URL + 'document/ranking?page={}'

class RankingScraper(object):

    MULTI_PROC  = 'exec multiprocess'
    THREAD_PROC = 'exec multithread'
    NO_PROC     = 'exec no multi process and thread'

    def __init__(self):
        pass

    def ranking(self, page):

        vtubers = []
        for p in range(page):

            # ランキングサイトのタグファクトリ生成
            factory = TagFactory(RANKING_URL.format(p + 1))

            # ランキングテーブルのタグ参照
            tag = factory.tag('table', {'class':'table-ranking'})

            # VTuber名称、順位、詳細ページURLを抽出
            for tr in tag.each('tr'):
                vtuber = {}
                vtuber[dbkey.VTUBER_OFFICE_KEY] = dbkey.UNKNOWN_TEXT
                vtuber[dbkey.VTUBER_TWITTER_KEY] = dbkey.UNKNOWN_TEXT
                vtuber[dbkey.VTUBER_YOUTUBE_KEY] = dbkey.UNKNOWN_TEXT
                vtuber[dbkey.VTUBER_NAME_KEY] = tr.child('img').alt().split('(')[0]
                vtuber[dbkey.VTUBER_RANK_KEY] = int(tr.strong().replace('位', ''))
                vtuber['url'] = tr.url()
                vtubers.append(vtuber)

        return vtubers

    def profiles(self, vtubers, exec_proc = NO_PROC):

        # VTuber詳細ページでプロフィール抽出

        # 通常実行
        if exec_proc == self.NO_PROC:
            for n in range(len(vtubers)):
                self._profile(vtubers[n])
            return vtubers

        # マルチスレッド実行
        elif exec_proc == self.THREAD_PROC:
            with ThreadPoolExecutor(max_workers=4, thread_name_prefix="thread")as executor:
                for n in range(len(vtubers)):
                    executor.submit(self._profile, vtubers[n])
            return vtubers

        # マルチプロセス実行
        elif exec_proc == self.MULTI_PROC:
            r_list = []
            with ProcessPoolExecutor() as executor:
                for n in range(len(vtubers)):
                    r_list.append(executor.submit(self._profile, vtubers[n]))

            u_vtubers = []
            for r in r_list:
                u_vtubers.append(r.result())
            return u_vtubers
        

    def _profile(self, vtuber):

        # プロフィールサイトのタグファクトリ生成
        factory = TagFactory(BASE_URL + vtuber['url'])

        # チャンネル情報全体のタグ参照
        tag = factory.tag('div', {'class': 'box-channel-info'})

        # VTuber所属オフィスを抽出
        try:
            vtuber[dbkey.VTUBER_OFFICE_KEY] = tag.child('img').alt().split('(')[0]
        except BSTagError as ex:
            print('failed to get {} office : {}'.format(vtuber[dbkey.VTUBER_NAME_KEY], ex.args))

        # チャンネル情報解析
        for tag in tag.each('div', {'class': 'channel-stat'}):

            # 全テキストを抽出し、各行(パラメータ)からファン数、総再生回数、Twitterを抽出
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

        return vtuber

