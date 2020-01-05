import db.dbkey as dbkey
from scraper.data_formatter import age
from scraper.tag_factory import TagFactory, BSTagError

KEY_MATCH = {'年齢': dbkey.VTUBER_AGE_KEY, '生年月日': dbkey.VTUBER_AGE_KEY,
                             '誕生日': dbkey.VTUBER_BIRTHDAY_KEY, '身長': dbkey.VTUBER_HEIGHT_KEY,
                             '身長・体重': dbkey.VTUBER_HEIGHT_KEY, 'Youtube':  dbkey.VTUBER_YOUTUBE_KEY, 'YouTube': dbkey.VTUBER_YOUTUBE_KEY,
                             'Fake年齢': dbkey.VTUBER_FAKE_AGE_KEY}


class NijisanjiScraper(object):
    def __init__(self, vtuber_name):
        self._vtuber_name = vtuber_name
        print('VTUBER = {}'.format(vtuber_name))

    def _find_vtuber_page(self, vtuber_list, factory):
        tag = factory.id('menubar').keyword('strong', vtuber_list).parent()
        for a in tag.each('a'):
            if a.text() == self._vtuber_name:
                return a.href()
        return None

    def _get_profile(self, url):
        factory = TagFactory('https://wikiwiki.jp/' + url)
        vtuber = {}
        vtuber[dbkey.VTUBER_NAME_KEY] = self._vtuber_name
        keyword_group = [('h3', 'プロフィール'), ('h2', 'プロフィール'), ('h2', '紹介')]
        for k in keyword_group:
            data_sets = self._get_profile_sub(factory, k)
            if data_sets:
                break

        for data in data_sets:
            match = [v for k, v in KEY_MATCH.items() if k == data[0]]
            if match:
                vtuber[match[0]] = data[1]

        if dbkey.VTUBER_AGE_KEY not in vtuber or vtuber[dbkey.VTUBER_AGE_KEY] == (-1):
            print('年齢推測')
            try:
                tag = factory.keyword('strong', '公式紹介文').parent()
                tag.dump()
                if tag:
                    vtuber[dbkey.VTUBER_AGE_KEY] = age(tag.text(), is_required=False)
                    if vtuber[dbkey.VTUBER_AGE_KEY] == -1:
                        tag = tag.parent()
                        tag.dump()
                        if tag:
                            vtuber[dbkey.VTUBER_AGE_KEY] = age(tag.text(), is_required=False)
            except BSTagError as ex:
                print('公式紹介文をうまくスクレイピングできない : {}'.format(ex.args))

        if dbkey.VTUBER_AGE_KEY not in vtuber or vtuber[dbkey.VTUBER_AGE_KEY] == (-1):
            print('年齢補完')
            if dbkey.VTUBER_FAKE_AGE_KEY in vtuber:
                vtuber[dbkey.VTUBER_AGE_KEY] = vtuber[dbkey.VTUBER_FAKE_AGE_KEY]

        return vtuber

    def _get_profile_sub(self, factory, keyword):
        print('パラメータスキャン開始')
        try:
            tag = factory.keyword(keyword[0], keyword[1])
            data_sets = []

            # キーワード以降のタグについて、３つ目までスキャンする。（直後のタグに年齢等が格納されているとは限らない。
            for i in range(3):
                tag = tag.next()
                print('-' * 80)
                tag.dump()
                data_sets = tag.param()
                print(data_sets)
                if data_sets:
                    break
        except BSTagError as ex:
            print('パラメータスキャン失敗 : {}'.format(ex.args))
            return []
        else:
            return data_sets

    def profile(self):
        vtuber = {}
        factory = TagFactory('https://wikiwiki.jp/nijisanji/')
        vtuber_list_group = ['一期生出身', '二期生出身', 'ゲーマーズ出身', 'SEEDs一期生出身',
                                                         'SEEDs二期生出身', '19年1～3月期生', '19年4～6月期生', '19年7～9月期生', '19年10～12月期生']

        for v in vtuber_list_group:
            page = self._find_vtuber_page(v, factory)
            if page:
                vtuber.update(self._get_profile(page))
                break
        return vtuber

if __name__ == '__main__':
    # print(NijisanjiScraper('樋口楓').profile())
    # print(NijisanjiScraper('エクス・アルビオ').profile())
    print(NijisanjiScraper('笹木咲').profile())
