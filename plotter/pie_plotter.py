#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd

from plotter.plotter import Plotter


class PiePlotter(Plotter):
    def __init__(self, db_path):
        super().__init__(db_path)

    def plot(self, output_column_name, unit):

        # 円グラフに出力したいカラムについて、その分布状況(にじさんじがxx件、ホロライブがyy件等))を集計。
        df_count = self._df[output_column_name].value_counts()

        # 円グラフのラベルと、実際の値をセット。
        labels = df_count.index.tolist()
        values = df_count.tolist()

        # 円グラフ描画。
        plt.title(output_column_name + ' 分布 (総計：{}{})'.format(sum(values), unit))
        plt.pie(values, labels=labels, shadow=True, autopct='%1.1f%%', wedgeprops=dict(width=0.5, edgecolor='w'))
        plt.show()

    def plot_by(self, output_column_name, collect_column_name):

        # 指定されたカラムについて、その分布状況(にじさんじがxx件、ホロライブがyy件等))を集計。
        df_count = self._df[collect_column_name].value_counts()


        # 円グラフに出力したいカラムについて、分布状況で取得した各データ毎(にじさんじ、ホロライブ等)に集計する。
        output_sets = {}
        for k, v in df_count.items():
            output_sets[k] = self._df[self._df[collect_column_name] == k][output_column_name].sum()

        # 円グラフのラベルと、実際の値をセット。
        labels = df_count.index.tolist()
        values = list(output_sets.values())
        plt.title(output_column_name + ' by ' + collect_column_name + ' (総計：{:,})'.format(sum(values)))
        plt.pie(values, labels=labels, shadow=True, autopct='%1.1f%%', wedgeprops=dict(width=0.5, edgecolor='w'))
        plt.show()
