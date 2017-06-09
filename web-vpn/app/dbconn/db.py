import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

data=conn.execute("select * from user")
# conn.commit()
for row in data:
    print(row)
print ("Records created successfully")
conn.execute("INSERT INTO user (user_id,group_id,user_name,user_pwd) VALUES (5,3,'even','even')")
conn.commit()

for tt in ea:
    print(tt)


conn.close()
def sql():
    aa=11