import sys

from scraper.ranking_scraper_thread import RankingScraper
from db.vtuber_rank_db import VTuberRankDB, AlreadyExistDBError
import db.dbkey as dbkey

# 引数取得(ランキングページ数)
args = sys.argv
if len(args) < 2:
    print('use filename ranking-page-count')
    sys.exit()

if not args[1].isdigit():
    print('ranking-page-count is not digit')
    sys.exit()
else:
    page_count = int(args[1])

# ランキングをスクレイピング
scraper = RankingScraper()
vtubers = scraper.ranking(page_count)
vtubers = scraper.profiles(vtubers, exec_proc=RankingScraper.MULTI_PROC)

# データベースへ格納
db = VTuberRankDB('./db/vtuber_rank.db')
for vtuber in vtubers:
    try:
        if vtuber[dbkey.VTUBER_VIEW_KEY] <= 0:
            continue
    except KeyError:
        print('this vtuber has no view data. {}'.format(vtuber))
        continue

    try:
        db.insert(
            vtuber[dbkey.VTUBER_NAME_KEY],
            vtuber[dbkey.VTUBER_OFFICE_KEY],
            vtuber[dbkey.VTUBER_RANK_KEY],
            vtuber[dbkey.VTUBER_FOLLOWER_KEY],
            vtuber[dbkey.VTUBER_VIEW_KEY],
            vtuber[dbkey.VTUBER_TWITTER_KEY],
            vtuber[dbkey.VTUBER_YOUTUBE_KEY])
    except AlreadyExistDBError:
        pass
