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
        cursor.execute("select state,update from lineuser where id = %s", (id,))
        try:
            data = cursor.fetchall()[0]
        except:
            data = None        
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
    
    def talk(self,id,msg):
        conn = psycopg2.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO linemsg (userid, message,time) VALUES (%s, %s,%s);", (id, msg,dt.now()))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected

if __name__ == "__main__":
    db = Database()
    print(db.get(13)==None)


