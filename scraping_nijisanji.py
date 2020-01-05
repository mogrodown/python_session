import pandas as pd
import sqlite3
from scraper.nijisanji_scraper import NijisanjiScraper


con = sqlite3.connect('./archive/vtuber.db')
df = pd.read_sql_query('SELECT * FROM vtuber_rank', con)

ns = df[df['office'] == 'にじさんじ']
print(ns['name'])

ns_top5_name = ns['name'][0:5]

vtubers = []
for n in ns_top5_name:
    vtubers.append(NijisanjiScraper(n).profile())

print(vtubers)

