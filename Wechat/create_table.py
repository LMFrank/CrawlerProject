import pymysql

db = pymysql.connect('localhost', 'root', 'password', 'wechat')
cursor = db.cursor()
sql = """CREATE TABLE spider (
         id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
         title VARCHAR(255) NOT NULL,
         content TEXT NOT NULL,
         date VARCHAR(255) NOT NULL,
         wechat VARCHAR(255) NOT NULL,
         nickname VARCHAR(255) NOT NULL,
         created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

cursor.execute(sql)
db.commit()
db.close()