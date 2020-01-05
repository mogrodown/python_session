from plotter.pie_plotter import PiePlotter
from plotter.bar_plotter import BarPlotter

'''
plotter = PiePlotter('./vtuber.db')
plotter.plot('office', '人')
plotter.plot_by('view', 'office')
'''

plotter = BarPlotter('./vtuber.db')
keywords = ['にじさんじ', 'ホロライブ', 'upd8', '.LIVE', 'unknown']
for k in keywords:
    plotter.plot('office', k, 'name', 'view')       # 視聴者数棒グラフ
    plotter.plot('office', k, 'name', 'follower')   # フォロワー数棒グラフ
plotter.plot_top_n('office', keywords, 'name', 'view', 10)
plotter.plot_top_n_sum('office', keywords, 'name', 'view', 10)
