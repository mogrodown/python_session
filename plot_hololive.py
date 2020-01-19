import pandas as pd
import yaml

from plotter.bar_plotter import BarPlotter
from scraper.nijisanji_scraper import NijisanjiScraper


NIJISANJI_YAML_PATH   = './db/nijisanji_db.yaml'

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
