from bs4 import BeautifulSoup
import requests
import re
import unicodedata


sentence = 'ゲーム配信をしているいつものしずりん。17歳。'

sentence = unicodedata.normalize('NFKC', sentence)
sentence = sentence.replace('(', '（').replace(')', '）')

import CaboCha
from cabocha.analyzer import CaboChaAnalyzer, EndOfLinkException
analyzer = CaboChaAnalyzer('-f1')
tree = analyzer.parse(sentence)

def is_STATE_FUKUSHI(chunk):
    print('check state fukushi: chunk={}'.format(chunk))
    if chunk.tokens[0].surface == '時':
        features = chunk.tokens[1].feature.split(',')
        if features[0] == '助詞' and features[1] == '係助詞':
            return True
    return False

def dump_token(chunk):
    for token in chunk:
        print('  {}'.format(token.feature))

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


# 係元が「しずりん」なので、「しずりん」の修飾(しずりんに係っているチャンク)を調べる。
for chunk in tree:
    try:
        if chunk.next_link == from_chunks[0]:
            break
    except EndOfLinkException:
        pass

print(chunk)
dump_token(chunk)

tgt_chunk = chunk
for chunk in tree:
    try:
        if chunk.next_link == tgt_chunk:
            print(chunk)
            dump_token(chunk)
            tgt_chunk = chunk
            break
    except EndOfLinkException:
        pass

for chunk in tree:
    try:
        if chunk.next_link == tgt_chunk:
            print(chunk)
            dump_token(chunk)
            tgt_chunk = chunk
            break
    except EndOfLinkException:
        pass

'''
if is_STATE_FUKUSHI(from_chunks[0]):
    # このチャンク(例：時は)は、状態副詞と係助詞の組み合わせ名なので、
    # このチャンクに係っている文節が、最終的にターゲットに係っていると推測できる。
    for chunk in tree:
        try:
            if chunk.next_link == from_chunks[0]:
                print('これが最終的に、年齢に係るチャンクである : {}'.format(chunk))
        except EndOfLinkException:
            pass
'''


