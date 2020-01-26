import sqlite3

if __name__ == '__main__':
    from vtuber_db import AlreadyExistDBError
else:
    from .vtuber_db import AlreadyExistDBError


CREATE = '''
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

INSERT = 'INSERT INTO vtuber_rank(name, office, rank, follower, view, twitter, youtube) \
           VALUES(\'{}\', \'{}\', {}, {}, {}, \'{}\', \'{}\');''' 

GET_ALL = 'SELECT * FROM vtuber_rank;'

DELETE = 'DELETE FROM vtuber_rank WHERE name=\'{}\';'

DELETE_ALL = 'DELETE FROM vtuber_rank;'

UPDATE_RANK = 'UPDATE vtuber_rank SET rank={} WHERE name=\'{}\';'



class VTuberRankDB(object):

    def __init__(self, db_path):
        self._con = sqlite3.connect(db_path)
        self._con.execute(CREATE)

    def insert(self, name, office, rank, follower, view, twitter, youtube):
        try:
            self._con.execute(INSERT.format(name, office, rank, follower, view, twitter, youtube))
            self._con.execute('COMMIT;')
        except sqlite3.IntegrityError:
            raise AlreadyExistDBError('ERROR : failed to insert cause already exists : %s' % name)

    def get_all(self):
        for item in self._con.execute(GET_ALL):
            print(item)

    def delete(self, name):
        self._con.execute(DELETE.format(name))
        self._con.execute('COMMIT;')

    def delete_all(self):
        self._con.execute(DELETE_ALL)
        self._con.execute('COMMIT;')

    def update_rank(self, name, rank):
        self._con.execute(UPDATE_RANK.format(rank, name))
        self._con.execute('COMMIT;')

    def __del__(self):
        self._con.close()

if __name__ == '__main__':
    db = VTuberRankDB('./test.db')
    db.delete_all()
    db.insert('ミライアカリ', 'personal', 1, 1000, 9999, 'twitter1', 'youtube1')
    db.get_all()
    # db.delete('ミライアカリ')
    # db.get_all()
    db.update_rank('ミライアカリ', 99)
    db.get_all()
