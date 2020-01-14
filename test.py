#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from scraper.ranking_scraper import RankingScraper
# vtubers = RankingScraper().get_ranking_data(1)
# print(vtubers)

import threading
import time

from concurrent.futures import ThreadPoolExecutor

'''
def print_time(name):
    print('name = {}'.format(name))
    time.sleep(1)

    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as ex:
        for i in range(5):
            ex.submit(print_time, 'mano')
'''


class A(object):
    def __init__(self):
        pass

    def get_data(self, vtubers):
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as ex:
            for i in range(5):
                ex.submit(self._print_time, vtubers['ミライアカリ'])

    def _print_time(self, vtuber):
        print('vtuber = {}'.format(vtuber))
        time.sleep(1)


a = A()
vtubers = {'ミライアカリ':17, 'シロ':18}
a.get_data(vtubers)
        



