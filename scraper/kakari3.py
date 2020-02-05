from bs4 import BeautifulSoup
import requests
import re
import unicodedata




import CaboCha
from cabocha.analyzer import CaboChaAnalyzer, EndOfLinkException

class MyCaboCha(object):

    def __init__(self, sentence):
        analyzer = CaboChaAnalyzer('-f1')
        sentence = unicodedata.normalize('NFKC', sentence)
        sentence = sentence.replace('(', '（').replace(')', '）')
        self._tree = analyzer.parse(sentence)

    def dump(self):
        for chunk in self._tree:
            print(chunk)

    def kakari_to(self, to_chunk):

        from_chunks = []
        for chunk in self._tree:
            try:
                if chunk.next_link == to_chunk:
                    from_chunks.append(chunk)
            except EndOfLinkException:
                pass
        return from_chunks

    def chunks(self):
        chunks = []
        for chunk in self._tree:
            chunks.insert(0, chunk)

        for chunk in chunks:
            yield chunk 

    @classmethod
    def dump_token(cls, chunk):
        for token in chunk:
            print(token)
            print('  {}'.format(token.feature))

# tree = MyCabo('一郎は二郎が描いた絵を三郎に贈った。')
# tree.dump()
# print(tree.kakari_to('贈った。'))

# tree = MyCaboCha('ゲーム配信をしているいつものしずりん。17歳。')
tree = MyCaboCha('しずりんの年齢は17歳です')
for chunk in tree.chunks():
    print('-' * 80)
    print('{} に係るチャンク = {}'.format(chunk, tree.kakari_to(chunk)))
    for c in tree.kakari_to(chunk):
        MyCaboCha.dump_token(c)

