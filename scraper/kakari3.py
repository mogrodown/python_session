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

    def is_unique_name(self):
        print('-' * 80)
        print(self._features)
        for f in self._features:
            if f[0] == '名詞' and f[1] == '固有名詞' and f[2] == '人名':
                print('OK')
                return True
        else:
            print('NG')
            return False

    def __str__(self):
        return self._token.feature


class MyChunk(object):

    def __init__(self, chunk):

        self._chunk = chunk
        self._tokens = [MyToken(t) for t in self._chunk.tokens]



    def is_FUKUSHI(self):
        pass
        '''
        if self._feat
            if features[0] == '名詞' and features[1] == '固有名詞' and features[2] == '人名':
                return True
        else:
            return False
        '''

    def is_equal_to(self, chunk):
        print('M = {}, to = {}'.format(self._chunk, chunk))
        return True if chunk.next_link == self._chunk else False

    def __iter__(self):
        for token in self._tokens:
            yield token
        else:
            raise StopIteration()


    def __str__(self):
        return self._chunk.surface


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
        
    def kakari_to(self, to_chunk):

        from_chunks = []
        for chunk in self._tree:
            try:
                if to_chunk.is_equal_to(chunk.next_link):
                    print('一致：{}, {}'.format(chunk.surface, to_chunk))
                    from_chunks.append(MyChunk(chunk))
            except EndOfLinkException:
                pass
        return from_chunks

    def chunks(self):
        chunks = []
        for chunk in self._tree:
            chunks.insert(0, chunk)

        for chunk in chunks:
            yield chunk 

    def search_chunk(self, formatter):
        for chunk in self._tree:
            if re.search(formatter, chunk.surface):
                return MyChunk(chunk)
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

cab = MyCaboCha('ゲーム配信をしているいつものしずりん。17歳。')

for chunk in cab:
    print('-' * 80)
    print(chunk)
    for token in chunk:
        print('  {}'.format(token))
        # print(token.is_unique_name())

# cab.dump()

'''
tgt_chunks = cab.search_chunk(FMT_AGE)
print(tgt_chunks)

from_chunks = cab.kakari_to(tgt_chunks)
print(from_chunks[0])

if from_chunks[0].is_chunk_unique_name():
    print('AA')


if from_chunks[0].is_chunk_unique_name():
    print('AA')
    from_chunks = cab.kakari_to(from_chunks[0])
    print(from_chunks)
    print(cab.dump_token(from_chunks[0]))
    '''

