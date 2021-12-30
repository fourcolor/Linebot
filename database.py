import os
import psycopg2
#databaseUrl = "postgres://mcaflkrdrretty:a666a34c4e398ad7fb5a605544c81f8879a40a05caef0b04b80fe553b0e57b98@ec2-52-72-252-211.compute-1.amazonaws.com:5432/d207a2go1qb9ti"

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a line-bot-fourcolor').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = conn.cursor()

SQL_order = '''我們輸入 SQL 指令的位置'''
cursor.execute(SQL_order)

conn.commit()

cursor.close()
conn.close()