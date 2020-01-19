import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import db.dbkey as dbkey
from scraper.data_formatter import age
from scraper.tag_factory import TagFactory, BSTagError

KEY_MATCH = {'年齢': dbkey.VTUBER_AGE_KEY, '生年月日': dbkey.VTUBER_AGE_KEY,
             '誕生日': dbkey.VTUBER_BIRTHDAY_KEY, '身長': dbkey.VTUBER_HEIGHT_KEY}

GROUP = ['所属タレント', '1期生', '2期生', 'ゲーマーズ', 'イノナカミュージック', '3期生'] # 4期生は12/27時点で未定


class NotFoundError(Exception):
    pass

class HololiveScraper(object):
    def __init__(self, name):
        self._name = name
        self._factory = TagFactory('https://seesaawiki.jp/hololivetv/')
        print('VTUBER = {}'.format(name))

        # 対象VTuberの詳細ページURLを検索
        for g in GROUP:
            self._url = self._search_url(g)
            if self._url:
                break
        else:
            raise NotFoundError('{} not found on page'.format(self._name))

    def _search_url(self, group):

        # タグ参照(グループ見出し(h3) => 親コンテナ => VTuberリスト)
        tag = self._factory.keyword('h3', group).parent().next()

        # 対象VTuberのリンクを返す
        for a in tag.each('a'):
            if a.text() == self._name:
                return a.href()
        return None

    def _profile(self):

        # 詳細ページの工場生成
        factory = TagFactory(self._url)

        # 基本情報参照
        tag = factory.keyword('h3', '基本情報').parent().next()

        # 基本情報からパラメータ(年齢、身長等)を抽出
        data_sets = tag.param()

        vtuber = {}

        # VTUBERによって取得できないパラメータもあるので、初期値を入れておく。
        vtuber[dbkey.VTUBER_BIRTHDAY_KEY]   = dbkey.UNKNOWN_TEXT
        vtuber[dbkey.VTUBER_AGE_KEY]        = -1
        vtuber[dbkey.VTUBER_HEIGHT_KEY]     = dbkey.UNKNOWN_TEXT

        vtuber[dbkey.VTUBER_NAME_KEY] = self._name

        # パラメータについて、ほしい情報のみ抽出
        for data in data_sets:
            match = [v for k, v in KEY_MATCH.items() if k == data[0]]
            if match:
                vtuber[match[0]] = data[1]

        # 年齢推測1
        if dbkey.VTUBER_AGE_KEY not in vtuber or vtuber[dbkey.VTUBER_AGE_KEY] == (-1):
            try:
                # 「概要」欄のタグ参照
                tag = factory.keyword('h3', '概要').parent().next()
                print(tag.text())

                import MeCab
                import unicodedata

                # tagger = MeCab.Tagger('-Ochasen')
                tagger = MeCab.Tagger('-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')

                tagger.parse('')  # 呪文。parseToNodeの前にparseしておくと、node.surfaceの文字化けが解消する。(UnicodeDecodeError: 'utf-8' codec can't decode...)
                node = tagger.parseToNode(unicodedata.normalize('NFKC', str(tag.text())))
                # print(tagger.parse(unicodedata.normalize('NFKC', str(tag.text()))))

                n = []
                while node:
                    if node.feature.startswith('名詞'):
                        if node.surface.startswith('年齢'):
                            if node.next.feature.startswith('助詞'):
                                print('AAAA = {}'.format(node.next.next.surface))
                    if node.feature.startswith('名詞') or node.feature.startswith('形容詞'):
                        n.append(node.surface)
                    node = node.next
                # print(n) 
                sys.exit()

                with open('./tmp.txt', 'w', encoding='utf-8') as f:
                    f.write(' '.join(n) + '\n')

                from gensim.models import word2vec
                s = word2vec.LineSentence('./tmp.txt')
                m = word2vec.Word2Vec(s,
                        sg=1,
                        size=300,
                        window=3,
                        min_count=1)
                # print(m.most_similar(positive='年齢', topn=20))
                # print(m.most_similar(positive='加入', topn=20))
                # tag.dump()
                if tag:
                    vtuber[dbkey.VTUBER_AGE_KEY] = age(tag.text(), is_required=False)
            except BSTagError as ex:
                print('概要をうまくスクレイピングできない : {}'.format(ex.args))

        # 年齢推測2
        if dbkey.VTUBER_AGE_KEY not in vtuber or vtuber[dbkey.VTUBER_AGE_KEY] == (-1):
            try:
                tag = factory.keyword('blockquote', '公式紹介文').parent()
                if tag:
                    vtuber[dbkey.VTUBER_AGE_KEY] = age(tag.text(), is_required=False)
            except BSTagError as ex:
                print('公式紹介文をうまくスクレイピングできない : {}'.format(ex.args))

        return vtuber

    def profile(self):

        # 詳細ページをスクレピング
        vtuber = {}
        vtuber.update(self._profile())
        return vtuber

if __name__ == '__main__':
    print(HololiveScraper('星街すいせい').profile())
