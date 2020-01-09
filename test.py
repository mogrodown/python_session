#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scraper.ranking_scraper import RankingScraper

vtubers = RankingScraper().get_ranking_data(1)
print(vtubers)

