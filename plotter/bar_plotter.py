import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd

from plotter.plotter import Plotter

class BarPlotter(Plotter):
    def __init__(self, data_frame=pd.DataFrame(), db_path=''):
        super().__init__(data_frame, db_path)

    def _show(self, title, x_items, y_items):
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.25, top=0.95)
        plt.xticks(rotation=270, size='small')

        plt.title(title)
        plt.bar(x_items, y_items)
        plt.show()

    def hist(self, column_name, upper_limit, interval):
        pd.cut(getattr(self._df, column_name), list(range(0, upper_limit, interval)), right=False).value_counts().sort_index().plot.bar(color='gray')
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.25, top=0.95)
        plt.show()

    def plot(self, x_column_name, y_column_name, collect_column_name = '', keyword = ''):

        print(collect_column_name)
        print(keyword)

        if collect_column_name:
            # 全データセットから、キーワードに一致するデータセットを抽出。
            df = self._df[self._df[collect_column_name] == keyword]
        else:
            df = self._df

        # 棒グラフ描画
        self._show(keyword + ' ' + y_column_name + '数',
                    list(df[x_column_name]),
                    list(df[y_column_name]))

    def plot_top_n(self, x_column_name, y_column_name, n, collect_column_name, keyword_list):

        # 全データセットから、キーワードリストそれぞれに一致するデータセットを抽出
        x_items = []
        y_items = []
        for k in keyword_list:
            df = self._df[self._df[collect_column_name] == k]
            x_items.extend(list(df[x_column_name])[0:n])
            y_items.extend(list(df[y_column_name])[0:n])

        # 棒グラフ描画
        self._show(y_column_name + ' 各オフィスTOP {}'.format(n),
                    x_items, y_items)

    def plot_top_n_sum(self, x_column_name, y_column_name, n, collect_column_name, keyword_list):

        # 全データセットから、キーワードリストそれぞれに一致するデータセットの総計を抽出
        x_items = []
        y_items = []
        for k in keyword_list:
            df = self._df[self._df[collect_column_name] == k]
            x_items.append(k)
            y_items.append(df[y_column_name].head(n).sum())

        # 棒グラフ描画
        self._show(y_column_name + ' 各オフィスTOP {}の合計'.format(n),
                    x_items, y_items)
