import pandas as pd
import sqlite3


class Plotter(object):
    def __init__(self, db_path):
        con = sqlite3.connect(db_path)
        pd.options.display.float_format='{:.2f}'.format
        self._df = pd.read_sql_query('SELECT * FROM vtuber_rank', con)
