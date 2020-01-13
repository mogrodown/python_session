import os
import pandas as pd
import sqlite3
import yaml

import db.dbkey as dbkey
from plotter.bar_plotter import BarPlotter
from scraper.nijisanji_scraper import NijisanjiScraper
from db.vtuber_profile_db import VTuberProfileDB

USE_DUMP = True
UNIT_TEST = False

if UNIT_TEST:
    nj = NijisanjiScraper('月ノ美兎')
    print(nj.profile())
    import sys
    sys.exit()

# pandas生成
df = pd.read_sql_query('SELECT * FROM vtuber_rank', sqlite3.connect('./vtuber_rank.db'))

# にじさんじのみ抽出
ns = df[df['office'] == 'にじさんじ']

# ns['name']で全データだが、ns['name'][0:5]とすることで先頭5件のみを処理できる。
# [v for v in vtubers if v and v['age'] <= 100]でフィルタリングすることもできる。

# ランキングから抽出した全にじさんじライバーの詳細情報抽出
vtubers = []
if not USE_DUMP:
    for n in ns['name']:
        # print(n)
        vtubers.append(NijisanjiScraper(n).profile())

    # 取得した情報をyamlファイルへ退避しておく。
    with open('nijisanji_profiles.yaml', 'w') as f:
        yaml.dump(vtubers, f, encoding='utf-8', allow_unicode=True)
else:
    with open('nijisanji_profiles.yaml', 'r') as f:
        vtubers = yaml.safe_load(f)

# DBに登録
os.remove('./nijisanji_profile.db')
db = VTuberProfileDB('./nijisanji_profile.db')
for v in vtubers:
    # print(v)
    try:
        db.insert(
            v[dbkey.VTUBER_NAME_KEY],
            v[dbkey.VTUBER_AGE_KEY],
            v[dbkey.VTUBER_HEIGHT_KEY],
            v[dbkey.VTUBER_BIRTHDAY_KEY])
    except KeyError:
        print('なんかおかしなデータ混ざった : {}'.format(v))

# データフレーム生成
df_vtubers = pd.DataFrame.from_dict(vtubers)
df_vtubers = df_vtubers.dropna(subset=['age', 'height'])
df_vtubers = df_vtubers[df_vtubers['age'] != 'unknown']
df_vtubers = df_vtubers[df_vtubers['height'] != 'unknown']

# 50歳以上のライバーをdf機能で絞り込み
print(df_vtubers[df_vtubers['age'] > 50])

# print(df_vtubers['height'].describe())
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
