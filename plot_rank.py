from plotter.pie_plotter import PiePlotter
from plotter.bar_plotter import BarPlotter

# オフィス分布
plotter = PiePlotter(db_path='./db/vtuber_rank.db')
plotter.plot('office', '人')
plotter.plot_by('view', 'office')

# オフィス毎指標
plotter = BarPlotter(db_path='./db/vtuber_rank.db')
keywords = ['にじさんじ', 'ホロライブ', 'upd8', '.LIVE', 'unknown']
for k in keywords:
    plotter.plot('name', 'view', 'office', k)       # 視聴者数棒グラフ
    plotter.plot('name', 'follower', 'office', k)   # フォロワー数棒グラフ
plotter.plot_top_n('name', 'view', 10, 'office', keywords)
plotter.plot_top_n_sum('name', 'view', 10, 'office', keywords)
