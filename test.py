#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from scraper.ranking_scraper import RankingScraper
# vtubers = RankingScraper().get_ranking_data(1)
# print(vtubers)

import threading
import time

def print_time(name):
    print('name = {}'.format(name))
    time.sleep(1)

threading.Thread(target=print_time, args=('Mano',)).start()
        



