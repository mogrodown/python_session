from bs4 import BeautifulSoup
import requests
import re
from scraper.data_formatter import age, height, birthday

class BSTagError(Exception):
    pass

class BSTag(object):
    def __init__(self, beautifulsoup_tag):
        if not beautifulsoup_tag:
            raise BSTagError('Failed to instance BSTag')
        self._tag = beautifulsoup_tag

    def dump(self):
        print(self._tag)

    def keyword(self, keyword_tag_name, keyword):
        tag = [tag for tag in self._tag.find_all(keyword_tag_name) if keyword in tag.text]
        if tag:
            return BSTag(tag[0])
        raise BSTagError('Not found keyword tag : {}'.format(keyword))

    def next(self):
        return BSTag(self._tag.find_next_sibling())

    def _param_iterator(self):
        if self._tag.name == 'ul' or self._tag.name == 'p':
            for line in self._tag.text.splitlines():
                yield line
        elif self._tag.name == 'div':
            for tr in self._tag.find_all('tr'):
                yield tr.text
        elif self._tag.name == 'table':
            for tr in self._tag.find_all('tr'):
                yield tr.text
        else:
            raise BSTagError('no iterator for this tag : {}'.format(self._tag.name))

    def param(self):
        data_sets = []
        for param in self._param_iterator():

            import MeCab
            import unicodedata
            tagger = MeCab.Tagger('-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
            tagger.parse('')
            # node = tagger.parseToNode(unicodedata.normalize('NFKC', param))
            node = tagger.parseToNode(param)
            print('-' * 80)
            print(param)
            while node:
                print(node)
                '''
                if node.feature.startswith('名詞'):
                    if node.surface.startswith('年齢'):
                        if node.next.feature.startswith('記号'):
                            print('年齢 = {}'.format(node.next.next.surface))
                '''
                node = node.next


            if '歳のとり方' in param or '歳はとる' in param:
                # 森中のややこしいパラメータ構造をうまく処理できてない。捨て。
                continue
            if '脳年齢' in param or 'バランス年齢' in param:
                continue  # 謎単位はとりあえず捨て。
            if param == '生年月日：西暦0年4月22日':
                continue  # うまく処理できず。捨て。

            if not re.search('[0-9]{1,30}', param):
                continue  # 数値データが含まれてない。捨て。

            if param.startswith('肉体年齢'):
                data_sets.append(('Fake年齢', age(param)))
            elif param.startswith('年齢') or param.startswith('ねんれい'):
                data_sets.append(('年齢', age(param)))
            elif param.startswith('身長'):
                data_sets.append(('身長', height(param)))
            elif param.startswith('誕生日') or param.startswith('たんじょび'):
                param = param.split('（')[0].split('(')[0] # ()の情報がややこしくなるので削除(月ノ美兎)
                if '年' in param:
                    data_sets.append(('年齢', age(param)))
                else:
                    data_sets.append(('誕生日', birthday(param)))
            elif param.startswith('学年'):
                data_sets.append(('年齢', age(param)))
            elif param.startswith('生年月日'):
                data_sets.append(('年齢', age(param)))
                data_sets.append(('誕生日', birthday(param)))

        return data_sets

    def prev(self, tag_name):
        return BSTag(self._tag.find_previous_sibling(tag_name))

    def child(self, tag_name, attrs=None):
        if attrs:
            return BSTag(self._tag.find(tag_name, attrs=attrs))
        else:
            return BSTag(self._tag.find(tag_name))

    def alt(self):
        return self._tag['alt']
        
    def atext(self):
        return self._tag.a.text

    def strong(self):
        return self._tag.strong.text

    def url(self):
        return self._tag['data-href']

    def href(self):
        return self._tag['href']

    def parent(self):
        return BSTag(self._tag.find_parent())

    def each(self, tag_name, attrs=None):
        if attrs:
            tag_list = self._tag.find_all(tag_name, attrs=attrs)
        else:
            tag_list = self._tag.find_all(tag_name)
        for tag in tag_list:
            yield BSTag(tag)

    '''
    def equal_text(self, text):
        return self._tag.text == text

    def url(self):
        try:
            return self._tag.a['href']
        except TypeError:
            return None
        '''


    '''
    def ahref(self):
        return self._tag.a['href']
        '''
    def text(self):
        return self._tag.text

class TagFactory(object):
    def __init__(self, url):
        print('Factory : URL : {}'.format(url))
        html = requests.get(url).text
        self._BS = BeautifulSoup(html, 'html.parser')

    def root_each(self, tag_name, callback, attrs=None):
        tag_list = self._BS.find_all(tag_name, attrs=attrs)
        for tag in tag_list:
            yield callback(BSTag(tag))

    def root_one(self, tag_name, attrs=None):
        return BSTag(self._BS.find(tag_name, attrs=attrs))

    def keyword_next_each(self, keyword_tag_name, keyword, tag_name, callback):
        keyword_tag = [tag for tag in self._BS.find_all(keyword_tag_name) if keyword in tag.text]
        if keyword_tag:
            for tag in keyword_tag[0].find_all_next(tag_name):
                yield callback(BSTag(tag))

    def keyword_next_one(self, keyword_tag_name, keyword, tag_name):
        keyword_tag = [tag for tag in self._BS.find_all(keyword_tag_name) if keyword in tag.text]
        if keyword_tag:
            return BSTag(keyword_tag[0].find_next(tag_name))

    def keyword_parent_one(self, keyword_tag_name, keyword):
        keyword_tag = [tag for tag in self._BS.find_all(keyword_tag_name) if keyword in tag.text]
        if keyword_tag:
            return BSTag(keyword_tag[0].find_parent())
        return None

    # =============================
    def keyword(self, keyword_tag_name, keyword):
        tag = [tag for tag in self._BS.find_all(keyword_tag_name) if keyword in tag.text]
        if tag:
            return BSTag(tag[0])
        raise BSTagError('Not found keyword tag : {}'.format(keyword))

    def id(self, id):
        tag = self._BS.find(id=id)
        if tag:
            return BSTag(tag)
        raise BSTagError('Not found id tag : {}'.format(id))

    def tag(self, tag_name, attrs=None):
        if attrs:
            return BSTag(self._BS.find(tag_name, attrs=attrs))
        else:
            return BSTag(self._BS.find(tag_name))

    def tag_each(self, tag_name, attrs=None):
        if attrs:
            for tag in self._BS.find_all(tag_name, attrs=attrs):
                yield BSTag(tag)
        else:
            for tag in self._BS.find_all(tag_name):
                yield BSTag(tag)

if __name__  == '__main__':
    factory = TagFactory('https://seesaawiki.jp/hololivetv/')
