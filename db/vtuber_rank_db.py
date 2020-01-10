# -*- coding: utf-8 -*-

import sqlite3
from .vtuber_db import AlreadyExistDBError

DBNAME = 'vtuber.db'
CRT_TBL = '''
    CREATE TABLE IF NOT EXISTS vtuber_rank
    (
        name TEXT NOT NULL UNIQUE,
        office TEXT NOT NULL,

        rank INTEGER NOT NULL,
        follower INTEGER NOT NULL,
        view INTEGER NOT NULL,
        twitter TEXT NOT NULL,
        youtube TEXT NOT NULL
    );
    '''
INS_TBL = '''
    INSERT INTO vtuber_rank(name, office, rank, follower, view, twitter, youtube)
    VALUES(?, ?, ?, ?, ?, ?, ?);''' 
SEL_ALL_TBL = '''SELECT * FROM vtuber_rank;'''

class VTuberRankDB(object):
    def __init__(self):
        self._con = sqlite3.connect(DBNAME)
        self._con.execute(CRT_TBL)
        # データ件数も少ないので、DB操作をカプセル化したカーソルは使用しない。

    def insert(self, name, office, rank, follower, view, twitter, youtube):
        try:
            self._con.execute(INS_TBL, (name, office, rank, follower, view, twitter, youtube))
            self._con.execute('COMMIT;')
        except sqlite3.IntegrityError:
            raise AlreadyExistDBError('ERROR : failed to insert cause already exists : %s' % name)

    def get_all(self):
        for item in self._con.execute(SEL_ALL_TBL):
            print(item)

    def __del__(self):
        self._con.close()

if __name__  == '__main__':
    db = VTuberRankDB()
    db.insert('ミライアカリ', 'personal', 1, 1000, 9999, 'twitter1', 'youtube1')
    db.get_all()
