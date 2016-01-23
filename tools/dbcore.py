import pymysql

conn = pymysql.connect(
    host='localhost',
    user='javaTest',
    password='123456',
    db='mydb',
    charset='utf8',
)


'''
cur = conn.cursor()

ans = cur.execute('select * from user')

print(cur.fetchall())
'''

