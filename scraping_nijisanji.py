import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import sqlite3
import yaml

import db.dbkey as dbkey
from plotter.bar_plotter import BarPlotter
from scraper.nijisanji_scraper import NijisanjiScraper

USE_DUMP    = False
UNIT_TEST   = False

RANK_DB_PATH        = './db/vtuber_rank.db'
NIJISANJI_YAML_PATH   = './db/nijisanji_db.yaml'

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

# 全ライバーの詳細抽出
vtubers = []
if not USE_DUMP:

    # 詳細抽出
    scrapers = []
    for n in ns['name']:
        vtubers.append(NijisanjiScraper(n).profile())

    # YAML保存
    try:
        os.remove(NIJISANJI_YAML_PATH)
    except FileNotFoundError:
        pass
    with open(NIJISANJI_YAML_PATH, 'w') as f:
        yaml.dump(vtubers, f, encoding='utf-8', allow_unicode=True)

else:
    # YAMLから詳細ロード
    with open(NIJISANJI_YAML_PATH, 'r') as f:
        vtubers = yaml.safe_load(f)

# データフレーム生成
df_vtubers = pd.DataFrame.from_dict(vtubers)
df_vtubers = df_vtubers.dropna(subset=['age', 'height'])
df_vtubers = df_vtubers[df_vtubers['age'] != 'unknown']
df_vtubers = df_vtubers[df_vtubers['height'] != 'unknown']

# 50歳以上のライバーをdf機能で絞り込み
# print(df_vtubers[df_vtubers['age'] > 50])

# 身長統計
print(df_vtubers['height'].min())
print(df_vtubers['height'].max())
print(df_vtubers['height'].mean())
print(df_vtubers['height'].std())

'''
# 年齢(500歳未満)プロット
df = df_vtubers[df_vtubers['age'] < 500]
plotter = BarPlotter(data_frame=df)
plotter.plot('name', 'age')

# 全員の身長プロット
plotter = BarPlotter(data_frame=df_vtubers)
plotter.plot('name', 'height')

# 100歳以下のヒストグラム
df = df_vtubers[df_vtubers['age'] < 100]
plotter = BarPlotter(data_frame=df)
plotter.hist('age', 100, 10)
'''
