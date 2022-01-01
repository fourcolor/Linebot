from logging import fatal
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime as dt

from werkzeug import datastructures
# Update connection string information
class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.dbname = os.getenv('DB_DATABASE')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASS')
        self.sslmode = "require"
        self.conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(self.host, self.user, self.dbname, self.password, self.sslmode)

    def insert(self,id,state):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lineuser (id, state) VALUES (%s, %s);", (id, state))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected

    def get(self,id):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("select state,update,trans_state,audio_enable,friend_enable,pairing_id from lineuser where id = %s", (id,))
        try:
            data = cursor.fetchall()[0]
        except:
            data = None        
        conn.commit()
        cursor.close()
        conn.close()
        return data

    def getUnpaired(self,id):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("select id,state,update,trans_state,audio_enable,friend_enable,pairing_id from lineuser where id != %s and pairing_id = '-1'", (id,))
        data = cursor.fetchall()      
        conn.commit()
        cursor.close()
        conn.close()
        return data

    def getUnpaired2(self,id1,id2):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("select id,state,update,trans_state,audio_enable,friend_enable,pairing_id from lineuser where id != %s and id != %s and pairing_id = '-1'", (id1,id2))
        data = cursor.fetchall()      
        conn.commit()
        cursor.close()
        conn.close()
        return data

    def update(self,id,state):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("update lineuser set state = %s ,update = %s where id = %s", (state,dt.now(),id))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected
    
    def talk(self,id,msg,to='-1'):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO linemsg (userid, message,time,to_id) VALUES (%s, %s,%s);", (id, msg,dt.now(),to))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected

    def updatelanguage(self,id,l):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("update lineuser set trans_state = %s ,update = %s where id != %s", (l,dt.now(),id))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected
    
    def updateAudio(self,id,l):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("update lineuser set audio_enable = %s ,update = %s where id = %s", (l,dt.now(),id))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected

    def pair(self,id1,id2):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("update lineuser set pairing_id = %s ,update = %s where id = %s", (id2,dt.now(),id1))
        affected = cursor.rowcount
        cursor.execute("update lineuser set pairing_id = %s ,update = %s where id = %s", (id1,dt.now(),id2))
        affected += cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected

    def talkHistory(self,id,pid):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("select id,userid,message,toid from linemsg where (userid = %s and pairing_id = %s) or (userid = %s and pairing_id = %s) orderby id", (id,pid,pid,id))
        data = cursor.fetchall()    
        conn.commit()
        cursor.close()
        conn.close()
        return data

    def rmPairing(self,id):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("update lineuser set pairing_id = %s ,update = %s where id = %s", ('-1',dt.now(),id))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected


if __name__ == "__main__":
    db = Database()
    print(db.getTransInfo('U11e740fda119861f84109438dfa63f38')[1]==False)


