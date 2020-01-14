#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraper.ranking_scraper_thread import RankingScraper
from db.vtuber_rank_db import VTuberRankDB, AlreadyExistDBError
import db.dbkey as dbkey

scraper = RankingScraper()
vtubers = scraper.ranking(1)
scraper.profiles(vtubers, exec_proc=RankingScraper.MULTI_PROC)
print(vtubers)


'''
db = VTuberRankDB('./vtuber_rank.db')
for vtuber in vtubers:
    if vtuber[dbkey.VTUBER_VIEW_KEY] <= 0:
        continue
    print(vtuber[dbkey.VTUBER_NAME_KEY])
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
'''
