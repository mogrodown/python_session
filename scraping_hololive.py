import os
import pandas as pd
import sqlite3
import yaml

from scraper.hololive_scraper import HololiveScraper, NotFoundError


RANK_DB_PATH            = './db/vtuber_rank.db'
HOLOLIVE_YAML_PATH     = './db/hololive_db.yaml'


# ランキングDBからデータフレーム作成
df = pd.read_sql_query('SELECT * FROM vtuber_rank', sqlite3.connect(RANK_DB_PATH))

# hololiveのみ抽出
ns = df[df['office'] == 'ホロライブ']

# スクレイパー駆動
vtubers = []
for n in ns['name']:
    try:
        vtubers.append(HololiveScraper(n).profile())
    except NotFoundError:
        pass

# YAML保存
try:
    os.remove(HOLOLIVE_YAML_PATH)
except FileNotFoundError:
    pass
with open(HOLOLIVE_YAML_PATH, 'w') as f:
    yaml.dump(vtubers, f, encoding='utf-8', allow_unicode=True)
