import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import db.dbkey as dbkey
from scraper.data_formatter import age
from scraper.tag_factory import TagFactory, BSTagError

KEY_MATCH = {'年齢': dbkey.VTUBER_AGE_KEY, '生年月日': dbkey.VTUBER_AGE_KEY,
             '誕生日': dbkey.VTUBER_BIRTHDAY_KEY, '身長': dbkey.VTUBER_HEIGHT_KEY,
             '身長・体重': dbkey.VTUBER_HEIGHT_KEY, 'Youtube':  dbkey.VTUBER_YOUTUBE_KEY,
             'YouTube': dbkey.VTUBER_YOUTUBE_KEY, 'Fake年齢': dbkey.VTUBER_FAKE_AGE_KEY}

GROUP = ['一期生出身', '二期生出身', 'ゲーマーズ出身', 'SEEDs一期生出身',
         'SEEDs二期生出身', '19年1～3月期生', '19年4～6月期生',
         '19年7～9月期生', '19年10～12月期生']


class NotFoundError(Exception):
    pass

class NijisanjiScraper(object):

    def __init__(self, name):
        self._name = name
        self._factory = TagFactory('https://wikiwiki.jp/nijisanji/')
        print('VTUBER = {}'.format(self._name))

        # 対象VTuberの詳細ページURLを検索
        for g in GROUP:
            self._url = self._search_url(g)
            if self._url:
                self._url = 'https://wikiwiki.jp/' + self._url
                break
        else:
            raise NotFoundError('{} not found on page'.format(self._name))

    def _search_url(self, group):

        # タグ参照(メニューコンテナ => グループ名 => VTuberリスト)
        tag = self._factory.id('menubar').keyword('strong', group).parent()

        # 対象VTuberのリンクを返す
        for a in tag.each('a'):
            if a.text() == self._name:
                return a.href()
        return None

    def _profile(self):

        # 詳細ページの工場生成
        factory = TagFactory(self._url)
        vtuber = {}

        # VTUBERによって取得できないパラメータもあるので、初期値を入れておく。
        vtuber[dbkey.VTUBER_BIRTHDAY_KEY]   = dbkey.UNKNOWN_TEXT
        vtuber[dbkey.VTUBER_AGE_KEY]        = -1
        vtuber[dbkey.VTUBER_HEIGHT_KEY]     = dbkey.UNKNOWN_TEXT

        vtuber[dbkey.VTUBER_NAME_KEY] = self._name

        # プロフィールは以下の３セット(タグ名, キーワード)のどこかに格納されている。
        search_sets = [('h3', 'プロフィール'), ('h2', 'プロフィール'), ('h2', '紹介')]

        for s in search_sets:
            data_sets = self._data_sets(factory, s)
            if data_sets:
                break

        # 取得したプロフィールについて、ほしい情報のみ抽出
        for data in data_sets:
            match = [v for k, v in KEY_MATCH.items() if k == data[0]]
            if match:
                vtuber[match[0]] = data[1]

        # 年齢推測１
        if dbkey.VTUBER_AGE_KEY not in vtuber or vtuber[dbkey.VTUBER_AGE_KEY] == (-1):
            try:
                # タグ参照
                tag = factory.keyword('strong', '公式紹介文').parent()
                if tag:

                    # 公式紹介文のテキストから年齢抽出
                    vtuber[dbkey.VTUBER_AGE_KEY] = age(tag.text(), is_required=False)

                    if vtuber[dbkey.VTUBER_AGE_KEY] == -1:

                        # 取得失敗なら、もう一階層上から抽出
                        tag = tag.parent()
                        if tag:
                            vtuber[dbkey.VTUBER_AGE_KEY] = age(tag.text(), is_required=False)
            except BSTagError as ex:
                print('公式紹介文をうまくスクレイピングできない : {}'.format(ex.args))

        # 年齢推測２
        if dbkey.VTUBER_AGE_KEY not in vtuber or vtuber[dbkey.VTUBER_AGE_KEY] == (-1):
            print('偽の年齢をとりあえず正規年齢とする')
            if dbkey.VTUBER_FAKE_AGE_KEY in vtuber:
                vtuber[dbkey.VTUBER_AGE_KEY] = vtuber[dbkey.VTUBER_FAKE_AGE_KEY]

        return vtuber

    def _data_sets(self, factory, search_set):

        try:
            # タグ参照
            tag = factory.keyword(search_set[0], search_set[1])

            data_sets = []

            # ３階層までスキャンする。(直後のタグに格納されているとは限らない)
            for i in range(3):
                tag = tag.next()

                 # 対象タグのパラメータ(年齢、身長等)を抽出
                data_sets = tag.param()
                if data_sets:
                    break

        except BSTagError as ex:
            print('パラメータスキャン失敗 : {}'.format(ex.args))
            return []
        else:
            return data_sets

    def profile(self):

        # 詳細ページをスクレピング
        vtuber = {}
        vtuber.update(self._profile())
        return vtuber

if __name__ == '__main__':
    # print(NijisanjiScraper('樋口楓').profile())
    print(NijisanjiScraper('森中花咲').profile())
    # print(NijisanjiScraper('エクス・アルビオ').profile())
    # print(NijisanjiScraper('笹木咲').profile())
