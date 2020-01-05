# -*- coding: utf-8 -*-

import sqlite3


class AlreadyExistDBError(Exception):
    pass

DBNAME = 'vtuber.db'
SEL_ALL_TBL = '''
    SELECT R.name, R.office, R.rank, R.follower, R.view, R.twitter, R.youtube, P.age, P.height, P.birthday
    FROM vtuber_rank AS R INNER JOIN vtuber_profile AS P ON R.name = P.name;'''

class VTuberDB(object):
    def __init__(self):
        self._con = sqlite3.connect(DBNAME)

    def get_all(self):
        for item in self._con.execute(SEL_ALL_TBL):
            print(item)

    def __del__(self):
        self._con.close()

if __name__  == '__main__':
    pass