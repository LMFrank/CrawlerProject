import pymysql

db = pymysql.connect('localhost', 'root', '199524', 'fangtianxia')
cursor = db.cursor()
sql1 = """CREATE TABLE newhouse (
         id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
         province VARCHAR(200) NOT NULL,
         city VARCHAR(200) NOT NULL,
         name VARCHAR(200) NOT NULL,
         house_type VARCHAR(200) NOT NULL,
         areas VARCHAR(200) NOT NULL,
         address VARCHAR(200) NOT NULL,
         district VARCHAR(200) NOT NULL,
         sale VARCHAR(200) NOT NULL,
         price VARCHAR(200) NOT NULL,
         detail_url VARCHAR(200) NOT NULL,
         created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

sql2 = """CREATE TABLE esfhouse (
         id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
         province VARCHAR(200) NOT NULL,
         city VARCHAR(200) NOT NULL,
         name VARCHAR(200) NOT NULL,
         house_type VARCHAR(200) NOT NULL,
         areas VARCHAR(200) NOT NULL,
         floor VARCHAR(200) NOT NULL,
         orientation VARCHAR(200) NOT NULL,
         year VARCHAR(200) NOT NULL,
         address VARCHAR(200) NOT NULL,
         total_price VARCHAR(200) NOT NULL,
         unit_price VARCHAR(200) NOT NULL,
         detail_url VARCHAR(200) NOT NULL,
         created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

cursor.execute(sql1)
cursor.execute(sql2)
db.commit()
db.close()