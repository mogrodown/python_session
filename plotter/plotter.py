import pandas as pd
import sqlite3


class PlotterError(Exception):
    pass

class Plotter(object):
    def __init__(self, data_frame, db_path):

        if not data_frame.empty:
            self._df = data_frame
        elif db_path:
            con = sqlite3.connect(db_path)
            pd.options.display.float_format='{:.2f}'.format
            self._df = pd.read_sql_query('SELECT * FROM vtuber_rank', con)
        else:
            raise PlotterError('invalid argument for constractor')
            
