from bs4 import BeautifulSoup
import requests
import re
from scraper.data_formatter import age, height, birthday


class MecabNode(object):

    def __init__(self, node):

        self.is_end = True

        if node:
            self._node = node
            self.text = node.surface
            self.detail = node.feature
            self.is_end = False

            # 品詞(part of speech)
            t = self.detail.split(',')
            self._POS = t[0:2]

    def next(self):
        return MecabNode(self._node.next) if self._node.next else None

    def prev(self):
        return MecabNode(self._node.prev) if self._node.prev else None

    def search(self, formula):
        return re.search(formula, self.text)

    def is_kakko_kai(self):
        if self._POS[0] == '記号' and self._POS[1] == '括弧開':
            return True
        return False

    def is_sentence_break(self):
        if self._POS[0] == 'BOS/EOS':
            return True
        return False
        # BOS : beginning of sentence
        # EOS : end of sentence

    def is_reading_point(self):
        # 、等の読点か否か判定。
        if self._POS[0] == '記号' and self._POS[1] == '読点':
            return True
        return False


class TextMining(object):

    def _is_transition(self, node):

        if not node.next.feature.startswith('記号'):
            return False, None

        if node.next.surface.startswith('→'):
            return True, node.next.next

        return False, None

    def _param_age(self, node):
        while node:
            if node.feature.startswith('名詞'):
                if node.surface.startswith('年齢'):
                    if node.next.feature.startswith('記号'):
                        age_node = node.next.next
                        print('年齢 1')
                    elif node.next.feature.startswith('名詞'):
                        age_node = node.next
                        print('年齢 2')
                    else:
                        print('ERRRRRRRRRRRRRRRRR')

                    result = self._is_transition(age_node)
                    while result[0]:
                        age_node = result[1]
                        result = self._is_transition(age_node)

                    print('年齢 ====== {}'.format(age_node.surface))

            node = node.next

    def find_kakari(self, chunk):

        is_kakari = False
        while not is_kakari:
            for token in chunk.tokens:
                fs = token.feature.split(',')
                print(fs)
                if fs[0] == '名詞' and fs[1] == '非自立':
                    continue
                if fs[0] == '助詞' or fs[0] == '記号' or fs[0] == '副詞':
                    continue
                if fs[0] == '記号':
                    continue
                is_kakari = True
                break
            else:
                chunk = chunk.prev_links[0]
        return chunk, token

    def _age_mining(self, node):

        while node:
            match = node.search('[0-9]{1,5}歳')
            if match:
                print('-' * 80)
                print(match[0])
                b = []
                prev = node.prev()
                while(prev):
                    # print(prev.text)
                    # 文頭、括弧開、読点(、)が見つかったら、遡るのをやめる。
                    if prev.is_sentence_break() or prev.is_kakko_kai() or prev.is_reading_point():
                        break
                    b.insert(0, prev.text)
                    prev = prev.prev()
                print(b)
                a = ''.join(b) + match[0] 
                print(a)

                # CaboChaでチャンク解析
                import CaboCha
                from cabocha.analyzer import CaboChaAnalyzer, EndOfLinkException
                analyzer = CaboChaAnalyzer('-f1')
                # parser = CaboCha.Parser('-n1')
                # parser = CaboCha.Parser('-f1')
                # tree = parser.parse(a)
                tree = analyzer.parse(a)
                target_token = None

                '''
                for chunk in tree:
                    for token in chunk:
                        print(token)
                '''

                target_chunk = None
                for chunk in tree:
                    if re.search('[0-9]{1,5}歳', chunk.surface):
                        target_chunk = chunk

                print('ターゲットチャンクは {}'.format(target_chunk.surface))
                is_param_format = False
                for token in target_chunk.tokens:
                    if '年齢' in token.surface:
                        is_param_format = True
                        break
                print(token, is_param_format)

                age = -1
                if is_param_format:
                    print('age = {}'.format(target_chunk.surface))
                    for token in target_chunk.tokens:
                        if token.surface.isnumeric():
                            age = int(token.surface)
                print(age)

                if age == (-1):
                    is_found = False
                    for chunk in tree:
                        try:
                            if chunk.next_link == target_chunk:
                                print('found chunk = {}, next = {}'.format(chunk, chunk.next_link))

                                kakari = self.find_kakari(chunk)
                                print('係元 = {}'.format(kakari))

                                fs = kakari[1].feature.split(',')
                                if not (fs[0] == '名詞' and fs[1] == '固有名詞' and fs[2] == '人名'):
                                    is_found = True
                                else:
                                    tgt = kakari[0]
                                    for c in tree:
                                        print(c, c.next_link)
                                        if c.next_link == tgt:
                                            print('bbbb')
                                            f = [t.feature for t in c]
                                            break
                                    verb = [a for a in f if a.split(',')[0] == '動詞']
                                    v_comp = False
                                    print('動詞 = {}'.format(verb))
                                    if verb:
                                        tgt = c
                                        for c in tree:
                                            print(c, c.next_link)
                                            if c.next_link == tgt:
                                                print('動詞にかかるチャンクは、{}'.format(c))
                                                print([t.feature for t in c])
                                                v_comp = True
                                                break
                                    else:
                                        tgt = c
                                        for c in tree:
                                            print(c, c.next_link)
                                            if c.next_link == tgt:
                                                print('bbbb')
                                                f = [t.feature for t in c]
                                                print(f)
                                                break

                                    if not v_comp:
                                        verb = [a for a in f if a.split(',')[0] == '動詞']
                                        print('動詞 = {}'.format(verb))
                                        if verb:
                                            tgt = c
                                            for c in tree:
                                                print(c, c.next_link)
                                                if c.next_link == tgt:
                                                    print('動詞にかかるチャンクは、{}'.format(c))
                                                    print([t.feature for t in c])

                        except EndOfLinkException:
                            pass



                '''
                if age == (-1):
                    print(target.prev_links)
                    
                    while (True):
                        for token in target.prev_links[0].tokens:
                            print(token.feature)
                            fs = token.feature.split(',')
                            if not (fs[0] == '名詞' and fs[1] ==  and fs[0] != '助詞':
                                break
                        else:
                            target = target.prev_links[0]
                            continue
                        print('qqq = {}'.format(token))
                        break
                '''
                        

                '''
                for chunk in tree:
                    try:
                        if chunk.next_link == target:
                            print('found chunk = {}, next = {}'.format(chunk, chunk.next_link))
                    except EndOfLinkException:
                        pass
                '''

                '''
                for i in range(tree.chunk_size()):
                    print('-' * 80)
                    chunk = tree.chunk(i)

                    # 現在のチャンクをトークンに分解して解析 ("ホロライブに" => "ホロライブ", "に")
                    for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
                        token = tree.token(j)
                        print('token = {}, {}'.format(token.surface, token.link))
                        if '歳' in token.surface:
                            target_token = (token, i)
                '''

                # print('target = {}, {}'.format(target_token[0].surface, target_token[1]))

                # print(tree.toString(CaboCha.FORMAT_TREE))
                # print(tree.toString(CaboCha.FORMAT_LATTICE))

            node = node.next()


    def __init__(self, text):

        import MeCab
        import unicodedata
        tagger = MeCab.Tagger('-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
        tagger.parse('')

        text = unicodedata.normalize('NFKC', text)
        text = text.replace('(', '（').replace(')', '）')

        node = MecabNode(tagger.parseToNode(text))

        # self._param_age(node)
        self._age_mining(node)

        

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

            mining = TextMining(param)

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
