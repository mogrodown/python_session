from bs4 import BeautifulSoup
import requests
import re
import unicodedata




import CaboCha
from cabocha.analyzer import CaboChaAnalyzer, EndOfLinkException

FMT_AGE = '[0-9]{1,5}歳'


class MyToken(object):

    def __init__(self, token):
        self._token = token
        self._features = token.feature.split(',')

    @property
    def feature(self):
        return self._features

    @property
    def surface(self):
        return self._token.surface

    def is_unique_name(self):
        if self._features[0] == '名詞' and \
           self._features[1] == '固有名詞' and \
           self._features[2] == '人名':
                return True
        else:
            return False

    def is_fukushi(self):
        return True if self._features[0] == '副詞' else False

    def is_jyoshi(self):
        return True if self._features[0] == '助詞' else False

    def is_doushi_jiritsu(self):
        return True if self._features[0] == '動詞' and self._features[1] == '自立' else False

    def is_meishi_sahen(self):
        return True if self._features[0] == '名詞' and self._features[1] == 'サ変接続' else False

    def is_state(self):
        # 状態を表す副詞
        return True if self._features[0] == '名詞' and self._features[1] == '非自立' and self._features[2] == '副詞可能' else False

    def __str__(self):
        return self._token.feature


class MyChunk(object):

    def __init__(self, chunk):

        self._chunk = chunk
        self._tokens = [MyToken(t) for t in self._chunk.tokens]


    @property
    def surface(self):
        return self._chunk.surface

    def search(self, formatter):
        return re.search(formatter, self._chunk.surface)

    def next(self):
        try:
            return MyChunk(self._chunk.next_link)
        except EndOfLinkException:
            return None

    def is_next_to(self, chunk):
        try:
            if self._chunk.next_link == chunk._chunk:
                return True
        except EndOfLinkException:
            return False
        else:
            return False

    def is_unique_name_phrase(self):
        return self._tokens[0].is_unique_name()

    def is_fukushi_phrase(self):
        return True if self._tokens[0].is_fukushi() and self._tokens[1].is_jyoshi() else False

    def is_doushi_phrase(self):
        if self._tokens[0].is_doushi_jiritsu():
            return True

    def is_meishi_sahen_doushi_phrase(self):
        # 「経営している」を判定。
        if self._tokens[0].is_meishi_sahen() and self._tokens[1].is_doushi_jiritsu():
            return True

    def is_state_phrase(self):
        return True if self._tokens[0].is_state() and self._tokens[1].is_jyoshi() else False

    def __iter__(self):
        for token in self._tokens:
            yield token
        else:
            raise StopIteration()


    def __str__(self):
        try:
            return '{} : next = {}'.format(self._chunk.surface, self._chunk.next_link)
        except EndOfLinkException:
            return '{} : next = None'.format(self._chunk.surface)


class MyCaboCha(object):

    def __init__(self, sentence):
        analyzer = CaboChaAnalyzer('-f1')
        sentence = unicodedata.normalize('NFKC', sentence)
        sentence = sentence.replace('(', '（').replace(')', '）')

        self._tree = analyzer.parse(sentence)
        self._chunks = [MyChunk(c) for c in self._tree.chunks]


    def __iter__(self):
        for chunk in self._chunks:
            yield chunk
        else:
            raise StopIteration()
        
    def kakari_to(self, to_chunk, reverse):
        chunks = []
        if reverse:
            for chunk in self._chunks:
                chunks.insert(0, chunk)
        else:
            chunks = self._chunks
            
        for chunk in chunks:
            if chunk.is_next_to(to_chunk):
                return chunk
        return None

    def chunks(self):
        chunks = []
        for chunk in self._tree:
            chunks.insert(0, chunk)

        for chunk in chunks:
            yield chunk 

    def search_chunk(self, formatter):
        for chunk in self._chunks:
            if chunk.search(formatter):
                return chunk
        return None

    def dump(self):

        for chunk in self._tree:
            print(chunk)

        for chunk in self._tree:
            print('-' * 80)
            print('{} に係るチャンク = {}'.format(chunk, self.kakari_to(chunk)))


    def dump_token(self, chunk):
        for token in chunk:
            print(token.feature)

# tree = MyCabo('一郎は二郎が描いた絵を三郎に贈った。')
# tree.dump()
# print(tree.kakari_to('贈った。'))

# cab = MyCaboCha('ゲーム配信をしているいつものしずりん。17歳。')
# cab = MyCaboCha('ロングヘアの時は 23歳')
# cab = MyCaboCha('動画編集やサムネイルの作成、アーカイブ整理をしているしずりん。17歳。')
# cab = MyCaboCha('「スナック凛」を経営しているしずりん。23歳')
cab = MyCaboCha('企業案件や収録等のお仕事をこなしているしずりん。23歳。')


for chunk in cab:
    print('-' * 80)
    print(chunk)
    for token in chunk:
        print('  {}'.format(token))

age_chunk = cab.search_chunk(FMT_AGE)
print('年齢chunk = {}'.format(age_chunk))

# 年齢チャンクが文脈の最後尾なら、解析は後方から実施する。
reverse = False
if not age_chunk.next():
    reverse = True


from_chunk = cab.kakari_to(age_chunk, reverse)
print('年齢に係るchunk = {}'.format(from_chunk))

# 固有名詞なら、それに係るチャンク検索
if from_chunk.is_unique_name_phrase():
    from_chunk = cab.kakari_to(from_chunk, reverse)
    print('固有名詞に係るchunk = {}'.format(from_chunk))
    goal = from_chunk.surface

# 副詞句なら、それに係るチャンク検索
if from_chunk.is_fukushi_phrase():
    from_chunk = cab.kakari_to(from_chunk, reverse)
    print('副詞に係るchunk = {}'.format(from_chunk))
    goal = from_chunk.surface
        
# 動詞句なら、それに係るチャンク検索
if from_chunk.is_doushi_phrase():
    from_chunk2 = cab.kakari_to(from_chunk, reverse)
    print('動詞句に係るchunk = {}'.format(from_chunk))
    goal = from_chunk2.surface + from_chunk.surface

if from_chunk.is_meishi_sahen_doushi_phrase():
    from_chunk2 = cab.kakari_to(from_chunk, reverse)
    print('名詞(サ変) + 動詞句に係るchunk = {}'.format(from_chunk))
    goal = from_chunk2.surface + from_chunk.surface
    
# 状態副詞なら、それに係るチャンク検索
if from_chunk.is_state_phrase():
    from_chunk2 = cab.kakari_to(from_chunk, reverse)
    print('状態副詞句に係るchunk = {}'.format(from_chunk))
    goal = from_chunk2.surface + from_chunk.surface


# アノテーション的作業。仕事を、が見つかれば、何の、を探す。
if '仕事を' in goal:
    from_chunk3 = cab.kakari_to(from_chunk2, reverse)
    goal = from_chunk3.surface + from_chunk2.surface
    

print('===> 年齢にかかる修飾子 = ' + goal)
