# -*- coding: utf-8 -*-

import sqlite3
from .vtuber_db import AlreadyExistDBError

DBNAME = 'vtuber.db'

CRT_TBL = '''
    CREATE TABLE IF NOT EXISTS vtuber_profile
    (
        name TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL,
        height INTEGER NOT NULL,
        birthday TEXT NOT NULL
    );
    '''
INS_TBL = '''
    INSERT INTO vtuber_profile(name, age, height, birthday)
    VALUES(?, ?, ?, ?);''' 
SEL_ALL_TBL = '''SELECT * FROM vtuber_profile;'''

class VTuberProfileDB(object):
    def __init__(self):
        self._con = sqlite3.connect(DBNAME)
        self._con.execute(CRT_TBL)

    def insert(self, name, age, height, birthday):
        try:
            self._con.execute(INS_TBL, (name, age, height, birthday))
            self._con.execute('COMMIT;')
        except sqlite3.IntegrityError:
            raise AlreadyExistDBError('ERROR : failed to insert cause already exists : %s' % name)

    def get_all(self):
        for item in self._con.execute(SEL_ALL_TBL):
            print(item)

    def __del__(self):
        self._con.close()


if __name__  == '__main__':
    db = VTuberProfileDB()
    db.insert('ミライアカリ', 17, 156, '12/5')
    db.get_all()
