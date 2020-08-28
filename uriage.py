import sqlite3

class Uriage:
    def __init__(self,uid,sid,kosu,hi) -> None:
        self.uid = uid
        self.sid = sid
        self.kosu = kosu
        self.hi = hi
    
    def __str__(self) -> str:
        return f"{self.uid=} {self.sid=} {self.kosu=} {self.hi=}"

class UriageDB:
    def __init__(self) -> None:
        dbname = 'hanbai.db'
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()
    
    def close(self):
        self.con.close()

    def find_by_sid(self,sid) -> list:
        self.cur.execute('SELECT * FROM uriage WHERE sid=?',[sid])
        rows = self.cur.fetchall()

        ret = []
        for row in rows:
            uid,sid,kosu,hi = row
            s = Uriage(uid,sid,kosu,hi)
            ret.append(s)
        
        return ret

    def insert(self,uriage):
        self.cur.execute('INSERT INTO uriage (sid,kosu,hi) VALUES(?,?,date("now"))',[uriage.sid,uriage.kosu])
        self.con.commit()


if __name__ == "__main__":
    db = UriageDB()

    u = Uriage(0,1,1,None)
    db.insert(u)

    all = db.find_by_sid(1)
    for u in all:
        print(u)

    db.close()