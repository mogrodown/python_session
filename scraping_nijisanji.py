import os
import pandas as pd
import sqlite3
import yaml

from scraper.nijisanji_scraper import NijisanjiScraper, NotFoundError


UNIT_TEST               = False

RANK_DB_PATH            = './db/vtuber_rank.db'
NIJISANJI_YAML_PATH     = './db/nijisanji_db.yaml'

# 単体テスト用
if UNIT_TEST:
    nj = NijisanjiScraper('月ノ美兎')
    print(nj.profile())
    import sys
    sys.exit()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ランキングDBを元に、ライバー情報を収集
#
# comment:
#   ns['name']で全データだが、ns['name'][0:5]とすることで先頭5件のみを処理できる。
#   [v for v in vtubers if v and v['age'] <= 100]でフィルタリングすることもできる。
#______________________________________________________________________________

# データフレーム作成
df = pd.read_sql_query('SELECT * FROM vtuber_rank', sqlite3.connect(RANK_DB_PATH))

# にじさんじのみ抽出
ns = df[df['office'] == 'にじさんじ']

# スクレイパー駆動、YAMLへ保存

vtubers = []
for n in ns['name']:
    try:
        vtubers.append(NijisanjiScraper(n).profile())
    except NotFoundError:
        pass

# YAML保存
try:
    os.remove(NIJISANJI_YAML_PATH)
except FileNotFoundError:
    pass
with open(NIJISANJI_YAML_PATH, 'w') as f:
    yaml.dump(vtubers, f, encoding='utf-8', allow_unicode=True)
