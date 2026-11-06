##ระบบลงชื่อเข้าออก พนักงาน

import sqlite3

##เชื่อมต่อฐานข้อมูล
conn= sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# 1. ลบตารางเก่าทิ้งก่อนเพื่อล้างข้อมูล 'peerapat' ที่ซ้ำกัน 4 ตัวออกไป
cursor.execute("DROP TABLE IF EXISTS user")

#สร้างตาราง 
cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    age INTEGER)''')

#เเทรกข้อมูลลงในตาราง
cursor.execute("INSERT INTO user (name, age) VALUES (?,?)", ('peerapat',25))
conn.commit()

data = [
    ('red', 15),
    ('green',17),
    ('bule' ,18),
    ('back' ,20)
]
cursor.executemany("INSERT INTO user (name, age) VALUES (?,?)",data)
conn.commit()


# 6 ลบข้อมูล 
cursor.execute("DELETE FROM user WHERE name = 'back'")
conn.commit()

cursor.execute("SELECT name , age FROM user")
rows = (cursor.fetchall())

# 5 เปลียนอายุ 
cursor.execute("UPDATE user SET age = ? WHERE name = ?", (30, 'peerapat'))
conn.commit()

print(rows)

conn.close()