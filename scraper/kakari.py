from bs4 import BeautifulSoup
import requests
import re
import unicodedata


sentence = 'ロングヘアの時は 23歳'

sentence = unicodedata.normalize('NFKC', sentence)
sentence = sentence.replace('(', '（').replace(')', '）')

import CaboCha
from cabocha.analyzer import CaboChaAnalyzer, EndOfLinkException
analyzer = CaboChaAnalyzer('-f1')
tree = analyzer.parse(sentence)

# xxの時は yy
# この構造が見つかったときは、yyにはxxが係っている。
# すなわち、「時は」は状態の副詞と、係助詞の組み合わせであるため、
# 「時は」の前と後を結び付けている。
# とりあえず「状態説明」と分類する。
#  時はCaboChanによると「副詞可能」とあるが、「状態の副詞」、「程度の副詞」、「陳述の副詞」のいずれかが判別できないため、
#  機械学習により、この三つのいずれかを前後の文節から判断できるようにしたい。
#  今は無理なので、「時」と、係助詞が組み合わさったら、「状態説明」分類に至る、「状態の副詞」と識別する。


def is_STATE_FUKUSHI(chunk):
    print('check state fukushi: chunk={}'.format(chunk))
    if chunk.tokens[0].surface == '時':
        features = chunk.tokens[1].feature.split(',')
        if features[0] == '助詞' and features[1] == '係助詞':
            return True
    return False

tgt_chunk = None
for chunk in tree:
    print(chunk)
    if re.search('[0-9]{1,5}歳', chunk.surface):
        tgt_chunk = chunk

print('ターゲット：{}'.format(tgt_chunk.surface))

from_chunks = []
for chunk in tree:
    try:
        if chunk.next_link == tgt_chunk:
            from_chunks.append(chunk)
    except EndOfLinkException:
        pass

print('係元: {}'.format(from_chunks))
for chunk in from_chunks:
    print('  chunk:{}'.format(chunk))
    for token in chunk:
        print('    {}, {}'.format(token, token.feature))

if is_STATE_FUKUSHI(from_chunks[0]):
    # このチャンク(例：時は)は、状態副詞と係助詞の組み合わせ名なので、
    # このチャンクに係っている文節が、最終的にターゲットに係っていると推測できる。
    for chunk in tree:
        try:
            if chunk.next_link == from_chunks[0]:
                print('これが最終的に、年齢に係るチャンクである : {}'.format(chunk))
        except EndOfLinkException:
            pass


