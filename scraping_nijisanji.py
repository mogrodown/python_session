import pandas as pd
import sqlite3
from scraper.nijisanji_scraper import NijisanjiScraper
from plotter.bar_plotter import BarPlotter


con = sqlite3.connect('./db/vtuber.db')
df = pd.read_sql_query('SELECT * FROM vtuber_rank', con)

ns = df[df['office'] == 'にじさんじ']
print(ns['name'])

vtubers = []

'''
ns_top5_name = ns['name'][0:5]
for n in ns_top5_name:
    vtubers.append(NijisanjiScraper(n).profile())
'''
'''
for n in ns['name']:
    vtubers.append(NijisanjiScraper(n).profile())

print(vtubers)
'''

vtubers = [{'name': '月ノ美兎', 'age': 16, 'height': 151, 'birthday': '9/24'}, {'name': '本間ひまわり', 'age': 19, 'height': 153}, {'name': '笹木咲', 'height': 148, 'age': 17, 'birthday': '11/11'}, {'name': '樋口楓', 'age': 17, 'height': 167}, {'name': '椎名唯華', 'birthday': '4/17', 'age': 16, 'height': 153}, {'name': '静凛', 'age': 17, 'height': 158, 'birthday': '8/28'}, {'name': '御伽 原江良', 'age': 24, 'height': 155, 'birthday': '7/28'}, {'name': '夢月ロア', 'age': 13, 'height': 141, 'birthday': '7/4'}, {'name': '鈴鹿詩子', 'age': 26, 'height': 159, 'birthday': '2/24'}, {'name': 'リゼ・ヘルエスタ', 'height': 166, 'birthday': '5/25', 'age': 17}, {'name': '緑仙', 'age': 17, 'height': 167, 'birthday': '4/16'}, {'name': '葛葉', 'age': 100, 'birthday': '11/10', 'height': 178}, {}, {'name': 'アンジュ・カトリーナ', 'birthday': '9/30', 'age': 27, 'height': 147}, {'name': '鈴原るる', 'age': 21, 'height': 162}, {'name': 'ベルモンド・バンデラス', 'height': 191, 'age': 10000000000, 'birthday': '11/3'}, {'name': '竜胆 尊', 'age': 9900, 'birthday': '10/20', 'height': 130}, {'name': '叶', 'age': -1, 'height': 175, 'birthday': '7/7'}, {'name': ' アルス・アルマル', 'age': 16, 'height': 147, 'birthday': '3/21'}, {'name': '郡道美玲', 'age': 20, 'height': 175, 'birthday': '6/14'}, {'name': '戌亥とこ', 'birthday': '9/9', 'age': 200, 'height': 162}, {'name': 'シスター・クレア', 'age': 21, 'birthday': '10/4'}, {'name': '社築', 'age': 28, 'height': 180, 'birthday': '11/23'}, {'name': '鷹宮リオン', 'height': 158, 'birthday': '1/7', 'age': 17}, {'name': 'ドーラ', 'age': 352, 'height': 175, 'birthday': '8/19'}, {'name': '物述有栖', 'age': 16, 'height': 143, 'birthday': '11/16'}, {'name': '勇気ちひろ', 'height': 138, 'birthday': '7/16', 'age': 10}, {'name': '森中花咲', 'age': 10, 'height': 135, 'birthday': '5/23'}, {'name': 'ジョー・力一', 'birthday': '10/1', 'age': -1}, {'name': 'エクス・アルビオ', 'age': 20, 'height': 180, 'birthday': '8/1'}, {'name': '黛灰', 'age': 22, 'height': 178}, {'name': '童田明治', 'age': 11, 'height': 147, 'birthday': '5/4'}, {'name': '剣持刀也', 'age': 16, 'height': 172, 'birthday': '8/22'}, {'name': '加賀美ハヤト', 'age': 28, 'height': 182}, {'name': '夜見れな', 'age': 15, 'birthday': '2/27'}, {}, {'name': 'でびでび・でびる', 'birthday': '12/18', 'age': -1}, {'name': '花畑チャイカ', 'age': 20}, {'name': '健屋花那', 'height': 163, 'birthday': '5/14', 'age': -1}, {'name': '宇志海いちご', 'birthday': '4/15', 'age': 8}, {'name': '舞元啓介', 'age': 34, 'height': 178, 'birthday': '11/9'}, {'name': '夢追 翔', 'age': 27, 'birthday': '6/28', 'height': 175}, {'name': '桜凛月', 'age': 19, 'birthday': '4/1', 'height': 150}, {'name': '家長むぎ', 'height': 154, 'age': 16, 'birthday': '11/7'}, {'name': '葉加瀬冬雪', 'age': 17, 'height': 152, 'birthday': '2/19'}, {'name': '三枝明那', 'age': 20, 'birthday': '9/1', 'height': 168}, {}, {'name': '卯月コウ', 'age': 13, 'birthday': '2/2', 'height': 157}, {'name': '星川サラ', 'birthday': '8/7', 'height': 155, 'age': -1}, {'name': '魔界ノりりむ', 'age': 10, 'birthday': '1/15', 'height': 110}, {'name': 'えま★おうがすと', 'age': 2477, 'birthday': '8/8', 'height': 138}, {'name': 'モイラ', 'age': 4600000000, 'height': 165, 'birthday': '2/10'}, {'name': '神田笑一', 'age': 22, 'birthday': '3/5', 'height': 175}, {'name': '夕陽リリ', 'age': 16, 'height': 162, 'birthday': '1/21'}, {'name': '相羽ういは', 'age': 19, 'birthday': '11/22', 'height': 167}, {'name': '雨森小夜', 'age': 17, 'birthday': '6/11'}, {'name': '赤羽葉子', 'age': 18, 'height': 168}, {'name': '愛園愛美', 'age': 21, 'birthday': '11/8', 'height': 154}, {'name': '黒井しば', 'birthday': '1/11', 'age': -1}, {'name': 'シェリン・バーガンディ', 'age': 27, 'height': 183, 'birthday': '1/6'}, {'name': '葉山舞鈴', 'age': 17, 'height': 158, 'birthday': '3/24'}, {'name': '早瀬走', 'age': 22, 'birthday': '3/20', 'height': 169}, {'name': '天宮こころ', 'height': 150, 'birthday': '7/1', 'age': -1}, {'name': '町田ちま', 'age': 16, 'birthday': '8/5', 'height': 150}, {'name': '出雲霞', 'age': 13, 'birthday': '10/13', 'height': 158}, {'name': 'エリー・コニファー', 'birthday': '9/27', 'height': 154, 'age': -1}, {'name': 'ラトナ・プティ', 'birthday': '10/14', 'height': 156, 'age': -1}, {'name': '伏見ガク', 'age': 20, 'height': 178, 'birthday': '10/5'}, {'name': 'ましろ', 'birthday': '4/27', 'age': 20, 'height': 165}, {'name': '不破湊', 'birthday': '4/18', 'age': 20, 'height': 173}, {'name': '白雪巴', 'birthday': '2/8', 'height': 174, 'age': -1}, {'name': '小野町春香', 'age': 15, 'height': 154}, {'name': 'フミ', 'age': 67, 'height': 176, 'birthday': '10/10'}, {'name': 'レヴィ・エリファ', 'birthday': '8/18', 'age': 6, 'fakeage': 20, 'height': 165}, {'name': '雪城眞尋', 'age': 15, 'birthday': '9/26', 'height': 151}, {'name': '文野環', 'age': -1}, {'name': '鈴谷アキ', 'age': 15, 'height': 155, 'birthday': '11/28'}, {'name': '鈴木勝', 'age': 19, 'height': 153}, {'name': '轟京子', 'height': 165, 'age': 20, 'birthday': '12/22'}, {'name': '瀬戸美夜子', 'age': 18, 'height': 158, 'birthday': '8/3'}, {'name': 'ギルザレンIII世', 'height': 195, 'birthday': '6/6', 'age': 4000}, {'name': 'ルイス・キャミー', 'birthday': '2/22', 'height': 168, 'age': -1}, {'name': '遠 北千南', 'age': 16, 'birthday': '10/30', 'height': 154}, {'name': '魔使マオ', 'height': 147, 'birthday': '5/31', 'age': 15}, {'name': '渋谷ハジメ', 'age': 20, 'height': 180, 'birthday': '5/5'}, {'name': '矢車りね', 'age': 11, 'height': 141}, {'name': '飛鳥ひな', 'age': 17, 'height': 145, 'birthday': '3/3'}, {'name': '安土桃', 'age': 14, 'birthday': '3/3', 'height': 142}, {'name': '山神カルタ', 'birthday': '8/11', 'age': -1}, {'name': 'グウェル・オス・ガール', 'height': 185, 'age': 2019}]

valid_vtubers = [v for v in vtubers if v and v['age'] <= 100]
df = pd.DataFrame.from_dict(valid_vtubers)
print(df)

plotter = BarPlotter(data_frame=df)
plotter.plot('name', 'age')

'''
vtubers = [{'name': '月ノ美兎', 'age': 16, 'height': 151, 'birthday': '9/24'}, {'name': '本間ひまわり', 'age': 19, 'height': 153}, {'name': ' 笹木咲', 'height': 148, 'age': 17, 'birthday': '11/11'}, {'name': '樋口楓', 'age': 17, 'height': 167}, {'name': '椎名唯華', 'birthday': '4/17', 'age': 16, 'height': 153}]
'''

