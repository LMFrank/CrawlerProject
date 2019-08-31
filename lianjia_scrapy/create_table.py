import pymysql

db = pymysql.connect('localhost', 'root', 'pwd', 'lianjia')
cursor = db.cursor()
sql = """CREATE TABLE spider (
         title VARCHAR(200),
         link VARCHAR(200),
         location VARCHAR(200),
         rent VARCHAR(200),
         apartment_layout VARCHAR(200),
         area VARCHAR(200),
         orientation VARCHAR(200),
         publish_time VARCHAR(200),
         unit_price FLOAT,
         floor VARCHAR(200),
         created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

cursor.execute(sql)
db.commit()
db.close()